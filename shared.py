from enum import Enum

GAME_STATE_INPUT_LENGTH = 40
GAME_STATE_INPUT_LENGTH = 38
SCREEN_HEIGHT = 239.0
SCREEN_WIDTH = 189.0
MAX_HEALTH = 176.0
MIN_MOVE = 1029
MAX_MOVE = 134218200

# emulator commands
class COMMAND_TYPE(Enum):
    RESET = "reset"
    PROCESSING = "processing"
    COMMAND = "command"

# valid controller buttons
class BUTTON(Enum):
    UP = "Up"
    DOWN = "Down"
    LEFT = "Left"
    RIGHT = "Right"
    B = "B" # weak kick
    A = "A" # medium kick
    R = "R" # strong kick
    Y = "Y" # weak punch
    X = "X" # medium punch
    L = "L" # strong punch

# valid button combinations
NO_ATTACK_DIRECTION_COMMANDS = [
    [BUTTON.UP,],
    [BUTTON.LEFT, BUTTON.UP],
    [BUTTON.RIGHT, BUTTON.UP]]

NO_KICK_DIRECTION_COMMANDS = [
    [BUTTON.LEFT, BUTTON.DOWN],
    [BUTTON.RIGHT, BUTTON.DOWN]]

ALL_ATTACK_DIRECTION_COMMANDS = [
    [],
    [BUTTON.LEFT,],
    [BUTTON.RIGHT,],
    [BUTTON.DOWN,]]

VALID_DIRECTION_COMMANDS = ALL_ATTACK_DIRECTION_COMMANDS + NO_ATTACK_DIRECTION_COMMANDS + NO_KICK_DIRECTION_COMMANDS

VALID_PUNCH_ATTACK_COMMANDS = [
    BUTTON.B,
    #BUTTON.A,
    BUTTON.R]

VALID_KICK_ATTACK_COMMANDS = [
    BUTTON.Y,
    #BUTTON.X,
    BUTTON.L]

VALID_COMMANDS = list(VALID_DIRECTION_COMMANDS)

for direction in ALL_ATTACK_DIRECTION_COMMANDS:
    for attack in VALID_PUNCH_ATTACK_COMMANDS + VALID_KICK_ATTACK_COMMANDS:
        new_command = list(direction)
        new_command.append(attack)
        VALID_COMMANDS.append(new_command)
        
for direction in NO_KICK_DIRECTION_COMMANDS:
    for attack in VALID_PUNCH_ATTACK_COMMANDS:
        new_command = list(direction)
        new_command.append(attack)
        VALID_COMMANDS.append(new_command)