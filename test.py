import retro
import retro.data  
import json
import struct
import sys
import logging
import time
from processText import process_move_menu_variables, process_text_box_variables, Decode, print_encoding_values
from pynput import keyboard
from pokemon import Pokemon

# TODO create and test a variable in the data.json track the number of moves each pokemon in our party has 
# TODO create and test a varible in the data.json to track the number of pokemon in our party
# https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Gold_and_Silver/RAM_map
# TODO create party class(consists of numPokemon Pokemon)
# TODO create pokemon class(consists of a pokemon with numMoves moves and all the pokemon's stats)
# TODO further investigate using bulbapedia API
# TODO further investigate using pokeAPI
# https://bulbapedia.bulbagarden.net/wiki/Special:ApiSandbox
# https://www.mediawiki.org/wiki/API:Main_page
# TODO create hardcoded type chart
# TODO create method makeDecision(info) which returns a decision
# this should be a move but in future we'll incorperate a switch and an item. 
# TODO create method completeDecision(decision, info) which returns a list of action arrays to accomplish the task
# in the future the second parameter will only contain text box info. That way it can tell where the cursor is pointed. 
# but first i need to figure out various text boxes. 
# TODO create method makeDecision(info) which returns a decision
# this should be a move but in future we'll incorperate a switch and an item. 
# TODO create method completeDecision(decision, info) which returns a list of action arrays to accomplish the task
# in the future the second parameter will only contain text box info. That way it can tell where the cursor is pointed. 
# but first i need to figure out various text boxes. 

game='PokemonSilver-GbColor'
data_path = "/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor/data.json"
scenario_path = "/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor/scenario.json"
env = retro.make(game, 'Battle.state') #in the Battle.state file we have 1 pokemon, Totodile, which is our current pokemon. 
env.reset()

# Define the action array
action = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # Default action with no buttons pressed

# Map keyboard keys to game actions
key_to_action = {
    'z': 0,      # B
    'tab': 2,    # SELECT
    'enter': 3,  # START
    'up': 4,     # UP
    'down': 5,   # DOWN
    'left': 6,   # LEFT
    'right': 7,  # RIGHT
    'x': 8       # A
}

# State to track pressed keys
keys_pressed = set()
exit_flag = [False]  # Use a mutable object to allow modification inside handlers


# Key press event handler
def on_press(key):
    try:
        key_str = key.char if hasattr(key, 'char') else key.name
        if key_str in key_to_action: 
            keys_pressed.add(key_str) 
        elif key_str == 'esc': # Leave loop when 'esc' is pressed
            exit_flag[0] = True
        elif key_str == 'i':  # Log information when 'i' is pressed
            log_game_info()
        elif key_str == 'm':  # Print menu information when 'm' is pressed
            menu_text_info() 
    except AttributeError:
        pass

# Key release event handler
def on_release(key):
    try:
        key_str = key.char if hasattr(key, 'char') else key.name
        if key_str in key_to_action and key_str in keys_pressed:
            keys_pressed.remove(key_str)
    except AttributeError:
        pass

# Logging function for game info
def log_game_info():
    logging.info(f"Captured info: {info}")
    print(f"Captured info: {info}")

def menu_text_info():
        decoded_menu_text = process_move_menu_variables(info)
        # Print the decoded menu text
        print(f"\n{decoded_menu_text}")

# Set up logging for game info
logging.basicConfig(filename='info_log.txt', level=logging.INFO, format='%(message)s')

# Start listening for keyboard inputs
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

done = False
i = 0
# ['B', None, 'SELECT', 'START', 'UP', 'DOWN', 'LEFT', 'RIGHT', 'A']
# main loop
while not done and not exit_flag[0]:
    env.render()

    #update the action array based on keys pressed
    action = [0] * 9 # Reset actions
    for key in keys_pressed:
        # see on_press(key) and key_to_action for all possible inputs
        action[key_to_action[key]] = 1 #set corresponding action to active

    # Perform the action in the environment
    obs, _, done, _, info = env.step(action)
    
listener.stop()
env.close()
print("Game loop exited.")