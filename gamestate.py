from shared import BUTTON, SCREEN_WIDTH, SCREEN_HEIGHT, MAX_HEALTH

class GameState():
    
    def __init__(self, raw_data, us, them):
        self.data = raw_data
        self.us = us
        self.them = them
        
        # if the players health goes to below 0 it changes it to 255
        # I'm reseting it to 0 so it doesn't screw up the models
        if self.us['health'] == 255:
            self.us['health'] = 0
            
        if self.them['health'] == 255:
            self.them['health'] = 0
       
    def is_between_rounds(self):
        return self.data['round_over'] and self.data['round_started'] and self.data['result'] in ('P1', 'P2')
    
    def is_match_complete(self):
        return self.data['round_over'] and not self.data['round_started']
    
    def get_input_features(self):
        return self.__get_input_features(self.data, self.us, self.them)
    
    def get_health_difference(self):
        return self.us['health'] - self.them['health']
        
    # Private
    def __get_input_features(self, game_state, us, them):
        features = [
            (game_state['width_delta'] - 94.5) / 94.5,
            (game_state['height_delta'] - 119.5) / 119.5,
            (game_state['timer'] - 76.5) / 76.5,
            (us['health'] - them['health']) / 176.0,
            int(us['buttons'][BUTTON.UP.value]),
            int(us['buttons'][BUTTON.DOWN.value]),
            int(us['buttons'][BUTTON.LEFT.value]),
            int(us['buttons'][BUTTON.RIGHT.value]),
            int(us['buttons'][BUTTON.A.value]),
            int(us['buttons'][BUTTON.B.value]),
            int(us['buttons'][BUTTON.X.value]),
            int(us['buttons'][BUTTON.Y.value]),
            int(us['buttons'][BUTTON.L.value]),
            int(us['buttons'][BUTTON.R.value]),
            (us['health'] - 88) / 88.0,
            int(us['in_move']),
            int(us['jumping']),
            int(us['crouching']),
            (us['x'] - 94.5) / 94.5,
            (us['y'] - 119.5) / 119.5,
            (them['health'] - 88) / 88.0,
            int(them['in_move']),
            int(them['jumping']),
            int(them['crouching']),
            (them['x'] - 94.5) / 94.5,
            (them['y'] - 119.5) / 119.5,
            ]
        
        character = [0] * 12
        character[them['character']] = 1
        
        return features + character
        
        """
        return [
            game_state['width_delta'],
            game_state['height_delta'],
            game_state['timer'],
            us['health'] - them['health'],
            int(us['buttons'][BUTTON.UP.value]),
            int(us['buttons'][BUTTON.DOWN.value]),
            int(us['buttons'][BUTTON.LEFT.value]),
            int(us['buttons'][BUTTON.RIGHT.value]),
            int(us['buttons'][BUTTON.A.value]),
            int(us['buttons'][BUTTON.B.value]),
            int(us['buttons'][BUTTON.X.value]),
            int(us['buttons'][BUTTON.Y.value]),
            int(us['buttons'][BUTTON.L.value]),
            int(us['buttons'][BUTTON.R.value]),
            us['health'],
            us['move'],
            int(us['in_move']),
            int(us['jumping']),
            int(us['crouching']),
            us['x'] / SCREEN_WIDTH,
            us['y'] / SCREEN_HEIGHT,
            them['character'],
            int(them['buttons'][BUTTON.UP.value]),
            int(them['buttons'][BUTTON.DOWN.value]),
            int(them['buttons'][BUTTON.LEFT.value]),
            int(them['buttons'][BUTTON.RIGHT.value]),
            int(them['buttons'][BUTTON.A.value]),
            int(them['buttons'][BUTTON.B.value]),
            int(them['buttons'][BUTTON.X.value]),
            int(them['buttons'][BUTTON.Y.value]),
            int(them['buttons'][BUTTON.L.value]),
            int(them['buttons'][BUTTON.R.value]),
            them['health'],
            them['move'],
            int(them['in_move']),
            int(them['jumping']),
            int(them['crouching']),
            them['x'],
            them['y'],
            them['character'],
            ]
        """