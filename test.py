import retro
import retro.data  
import json
import struct
import sys
import logging
import time
import asyncio
import queue
from action_ai import get_action_queue
from processText import process_move_menu_variables, Decode, print_encoding_values
from pynput import keyboard
from pokemon import Pokemon
from decision_ai import make_decision
from functools import partial

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
# TODO create a method called create pokemon data


# Logging function for game info
def log_game_info(shared_state):
    info = shared_state.get("info", {})
    logging.info(f"Captured info: {info}")
    print(f"Captured info: {info}")

def menu_text_info(shared_state):
        info = shared_state.get("info", {})
        decoded_menu_text = process_move_menu_variables(info)
        # Print the decoded menu text
        print(f"\n{decoded_menu_text}")

# Set up logging for game info
logging.basicConfig(filename='info_log.txt', level=logging.INFO, format='%(message)s')

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

# Key press event handler
def on_press(key, shared_state):
    try:
        key_str = key.char if hasattr(key, 'char') else key.name
        if key_str in key_to_action: 
            shared_state["keys_pressed"].add(key_str) 
        elif key_str == 'esc': # Leave loop when 'esc' is pressed
            shared_state["exit_flag"] = True
        elif key_str == 'i':  # Log information when 'i' is pressed
            log_game_info(shared_state)
        elif key_str == 'm':  # Print menu information when 'm' is pressed
            menu_text_info(shared_state) 
    except AttributeError:
        pass

# Key release event handler
def on_release(key):
    try:
        key_str = key.char if hasattr(key, 'char') else key.name
        if key_str in key_to_action and key_str in shared_state["keys_pressed"]:
            shared_state["keys_pressed"].remove(key_str)
    except AttributeError:
        pass    

import asyncio
from collections import deque

action_queue = deque()
action_taken = False  # State variable to track if an action has been taken

# Define shared state
shared_state = {
    'info': None,
    'exit_flag': False,
    'keys_pressed': set(),
    'action_taken': False,
    'move_taken': False
}

# Start listening for keyboard inputs
listener = keyboard.Listener(on_press=partial(on_press, shared_state=shared_state), on_release=on_release)
listener.start()

async def render_environment(env, shared_state):
    """Task to render the environment and handle inputs."""
    while not shared_state["exit_flag"]:
        #env.render()

        # Update action array based on keys pressed
        action = [0] * 9
        for key in shared_state["keys_pressed"]:
            action[key_to_action[key]] = 1
        
        # Perform the action in the environment
        _, _, done, _, shared_state["info"] = env.step(action)

        # Stop if done
        if done:
            shared_state["exit_flag"] = True

        await asyncio.sleep(1/60)  # Adjust as necessary

async def check_determinator(env, shared_state):
    """Task to check info['determinator'] and make AI decisions."""
    action_taken = shared_state["action_taken"]
    move_taken = shared_state["move_taken"]
    while not shared_state["exit_flag"]:
        _, _, _, _, shared_state["info"] = env.step([0] * 9)  # Fetch latest info without doing any action
        

        action_taken = shared_state["action_taken"]
        move_taken = shared_state["move_taken"]
        info = shared_state["info"]
        menu_str = process_move_menu_variables(info)
        #print(menu_str)
        if info and info.get("determinator") == 121 and not action_taken:
            await asyncio.sleep(0.5)
            print(f"Making decision based on determinator. \n Menu state:\n{menu_str}")
            action = [0] * 9
            #action[8] = 1  # Example action: press 'A'
            #action_queue.append(action)  # Queue the action
            #action_queue.append(action)  # Queue the action
            action_taken = True  # Set action taken to True
            # def get_action_queue(action_description, menu_state):
            action_arr = get_action_queue("Choose the move scratch", menu_str)
            for actions in action_arr:
                action[actions] = 1
                action_queue.append(action)
                action = [0] * 9 
            # Allow some time for the game to process the action
            await asyncio.sleep(3)  # Adjust this delay based on how long you need
            
        elif info and info.get("move_determinator") == 126 and not action_taken and info.get("determinator") != 121 and not move_taken:
            await asyncio.sleep(0.5)
            print(f"Making decision based on move determinator. \n Menu state\n{menu_str}")

            action = [0] * 9
            #action[8] = 1  # Example action: press 'A'
            #action_queue.append(action)  # Queue the action
            #action_queue.append(action)  # Queue the action
            move_taken = True  # Set action taken to True
            # def get_action_queue(action_description, menu_state):
            action_arr = get_action_queue("Choose the move scratch", menu_str)
            for actions in action_arr:
                action[actions] = 1
                action_queue.append(action)
                action = [0] * 9 

            #print("Finished adding ")
            # Allow some time for the game to process the action
            await asyncio.sleep(3)  # Adjust this delay based on how long you need

        #we still need to process actions when move determinator == 126
        elif info.get("determinator") != 121 and action_taken:
            # need second determinator, go find the top left corner of the box and  see if its a NE right corner or ES
            action_taken = False  # Reset action_taken when determinator changes
            print("reset action taken")
            #move_taken ?
        elif info.get("move_determintator") != 126 and move_taken:
            move_taken = False
            print("reset move taken")

        await asyncio.sleep(0.1)  # Control how often to check
    print("end determinator")

async def process_actions(env, shared_state):
    """Task to process actions from the queue."""
    #print(shared_state["exit_flag"])
    while not shared_state["exit_flag"]:
        action_taken = shared_state["action_taken"]
        move_taken = shared_state["move_taken"]
        while action_queue:  # Process all available actions
            #env.render()
            action = action_queue.popleft()  # Get the next action from the queue
            _, _, done, _, shared_state["info"] = env.step(action)

            print(f'action taken{action}')
            await asyncio.sleep(1)  # Control the rate of processing actions
        
            if done:
                shared_state["exit_flag"] = True
                break
        #print("complete action queue")
        if action_taken or move_taken:
            shared_state["shared_state"] = False
            shared_state["move_taken"] = False
        await asyncio.sleep(1)  # Control the rate of processing actions    
    print("end process")
        

async def main(env):
    """Main function to run tasks concurrently."""
    await asyncio.gather(
        render_environment(env,shared_state),
        check_determinator(env,shared_state),
        process_actions(env, shared_state)
    )

asyncio.run(main(env))