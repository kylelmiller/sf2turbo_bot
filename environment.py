import socket
import json
import gamestate
import random
import gym
import numpy as np

from shared import *
from gym import spaces

BUFSIZE = 1024

SAVE_STATES = ["SNES/State/ryu_chunli.State",
               "SNES/State/ryu_blanka.State",
               "SNES/State/ryu_dhalsim.State",
               "SNES/State/ryu_ehonda.State",
               "SNES/State/ryu_ryu.State",
               "SNES/State/ryu_ken.State",
               "SNES/State/ryu_zang.State",
               "SNES/State/ryu_balrog.State",
               "SNES/State/ryu_guile.State",
               #"SNES/State/ryu_vega.State", Vega is really different, has invuln on the wall
               ]

class Environment(gym.Env):
    
    def __init__(self, us='p1', them='p2', skip_frames=2, host='0.0.0.0', port=9999, save_file_location='random', history=4):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.us = us
        self.them = them
        self.command_queue = []
        self.previous_health_difference = 0
        self.previous_reward = 0
        self.skip_frames = skip_frames
        self.save_file_location = save_file_location
        self.history = history
        
        # Set these in ALL subclasses
        self.action_space = spaces.Discrete(len(VALID_COMMANDS)) 
        self.observation_space = spaces.Box(low=-1, high=1, shape=(GAME_STATE_INPUT_LENGTH*history,))
        
        self._connect(host, port)
        
    # gym overrides
    def _step(self, action):
        self._issue_command(VALID_COMMANDS[action])
        game_state, reward = self._receive()
        self.obsevations = self.obsevations[GAME_STATE_INPUT_LENGTH:] + game_state.get_input_features()
        return np.array(self.obsevations), float(reward), game_state.is_between_rounds() or game_state.is_match_complete(), {}
        
    def _reset(self):
        self._load_save(self.save_file_location)
        game_state, reward = self._receive()
        self.obsevations = []
        for _ in range(self.history):
            self.obsevations.extend(game_state.get_input_features())
        return np.array(self.obsevations)
        
    def _close(self):
        self.conn.close()
        
    # other private methods            
    def _connect(self, host='0.0.0.0', port=9999):
        self.serversocket.bind((host,port))
        self.serversocket.listen()
        print("listening")
        
        self.conn, self.addr = self.serversocket.accept()
      
    
    def _load_save(self, save_file_location):
        # issue the command
        command = self._get_base_command()
        
        command["type"] = COMMAND_TYPE.RESET.value
        if save_file_location == "random":
            command['savegamepath'] = random.choice(SAVE_STATES)
        else:
            command['savegamepath'] = save_file_location
        self._send_to_emulator(command)
        
    def _receive_game_state(self):        
        # receive the game state
        data = self.conn.recv(BUFSIZE)
        if not data: 
            return None, None
                
        # load the game state
        raw_data = json.loads(data.decode('ascii'))
        return gamestate.GameState(raw_data, raw_data[self.us], raw_data[self.them])
        
    def _receive(self):
        # before passing on a received game state we need to clear out our command backlog
        while len(self.command_queue):
            data = self.conn.recv(BUFSIZE)
            if not data: 
                return None, None
            
            self._send_to_emulator(self.command_queue[0])
            del self.command_queue[0]
        
        # receive the current game state        
        game_state = self._receive_game_state()
        
        # we skip frames until we can issue a valid command again
        if game_state.us['jumping'] and game_state.us['in_move']:
            while game_state.us['jumping']:
                self._send_to_emulator(self._get_base_command())
                game_state = self._receive_game_state()
        
        # calculate the reward from the previous command
        #previous_reward = self.previous_health_difference - game_state.get_health_difference()
        #self.previous_health_difference = game_state.get_health_difference()
        
        # return the game state
        new_health_difference = game_state.get_health_difference() - self.previous_health_difference 
        self.previous_health_difference = game_state.get_health_difference()
        reward = 0
        if game_state.data['result'].lower() == self.us.lower():
            reward = 1
        elif game_state.data['result'].lower() == self.them.lower():
            reward = -1
        return game_state, new_health_difference / 176.0
    
    def _issue_command(self, buttons):
        command = self._get_base_command()
        # we are in a round, fight
        command["type"] = COMMAND_TYPE.COMMAND.value
        
        for button in buttons:
            command[self.us][button.value] = True
        
        # we only want to issue a button command every 3 frames
        if len([button for button in buttons if button in ALL_VALID_ATTACK_COMMANDS]):
            multiplier = 6
        else:
            multiplier = 1
        for _ in range(self.skip_frames*multiplier):
            self.command_queue.append(command)
        self._send_to_emulator(command)
    
    
    def _send_to_emulator(self, command):
        self.conn.send(json.dumps(command).encode())
        
    def _get_base_command(self):
        return {"type": "", "p1": {}, "p2": {}, "player_count": 1, "savegamepath": False }
