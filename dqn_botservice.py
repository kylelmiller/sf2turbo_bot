import environment
import dqn
import argparse
import random

from shared import *
from baselines import deepq
import pickle as pkl
import pandas as pd

LOCATION_X_MAX = 500
LOCATION_X_MIN = 0
    
def callback(lcl, glb):
    # stop training if reward exceeds 0.7
    is_solved = lcl['t'] > 100 and sum(lcl['episode_rewards'][-101:-1]) / 100.0 >= .8
    return is_solved
   
def record_game_states():
    parser = argparse.ArgumentParser("Run a Street Fighter 2 Turbo bot")
    parser.add_argument('--port', dest='port', type=int, default=9999)
    parser.add_argument('--save', dest='save_location', default="random")
    parser.add_argument('--player1', dest='player1', default="True")
    parser.add_argument('--train', dest='train', default="True")
    args = parser.parse_args()
    
    if args.player1 == "True":
        us = 'p1'
        them = 'p2'
    else:
        us = 'p2'
        them = 'p1'    
        
    env = environment.Environment(us=us, them=them, skip_frames=3, port=args.port)
        
    game_states = []
    for i in range(2000):
        env.reset()
        
        done = False
        
        while not done:
            action = random.choice(range(len(VALID_COMMANDS)))
            #action = VALID_COMMANDS.index([BUTTON.UP,])
        
            observation, reward, done, metadata = env.step(action)
        
            game_states.append(observation[-GAME_STATE_INPUT_LENGTH:])
        
    pkl.dump(game_states, open("game_states.pkl", 'wb'))
   
def load_recorded_game_states():
    game_states = pkl.load(open("game_states.pkl", 'rb'))
    df = pd.DataFrame(game_states)
    pd.set_option('display.max_columns', 50)
    print(df.describe())
    return
   
def main(): 
    parser = argparse.ArgumentParser("Run a Street Fighter 2 Turbo bot")
    parser.add_argument('--port', dest='port', type=int, default=9999)
    parser.add_argument('--save', dest='save_location', default="random")
    parser.add_argument('--player1', dest='player1', default="True")
    parser.add_argument('--train', dest='train', default="True")
    args = parser.parse_args()
    
    if args.player1 == "True":
        us = 'p1'
        them = 'p2'
    else:
        us = 'p2'
        them = 'p1'        
    
    env = environment.Environment(us=us, them=them, skip_frames=3, port=args.port, history=4, save_file_location="SNES/State/ryu_blanka.State")
    model = deepq.models.mlp([512, 512,])
    act = deepq.learn(
        env,
        q_func=model,
        lr=1e-3,
        max_timesteps=700000,
        buffer_size=50000,
        exploration_fraction=0.1,
        exploration_final_eps=0.02,
        gamma=0.9,
        learning_starts=5000,
        print_freq=10,
        callback=callback
    )
    print("Saving model to sf2_model.pkl")
    act.save("sf2_model.pkl")
    
    
if __name__ == "__main__":
    #load_recorded_game_states()
    #record_game_states()
    main()
    
def junk():
    """
    #accept connections from outside
    env.connect(port=args.port)
    
    game_state, previous_reward = env.receive()
    env.load_save(args.save_location)
    game_state, previous_reward = env.receive()
    model.setInitState(game_state.get_input_features())
    
    while True:        
        
        # the client closed the connection
        if not game_state:
            break
                            
        action = model.getAction()
        game_state, reward = env.step(VALID_COMMANDS[list(action).index(1)])
        model.setPerception(game_state.get_input_features(), action, reward, game_state.is_between_rounds() or game_state.is_match_complete())
        
        # 3 rounds in a match, wait for next round
        # match is over, reload
        if game_state.is_between_rounds() or game_state.is_match_complete():
            env.no_op()
            # load the game state
            game_state, previous_reward = env.receive()
            
            env.load_save(SAVE_STATE)
            # load the game state
            game_state, previous_reward = env.receive()
            
            env.load_save(args.save_location)
            # load the game state
            game_state, previous_reward = env.receive()
            model.setInitState(game_state.get_input_features())
                
    env.close()
    """