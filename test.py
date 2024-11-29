import retro
import retro.data  
import json
import struct
import sys
import logging
import time
import asyncio
import queue
from processText import process_move_menu_variables, Decode, print_encoding_values
from pynput import keyboard
from pokemon import Pokemon
from decision_ai import make_decision

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

# Set up logging for game info
logging.basicConfig(filename='info_log.txt', level=logging.INFO, format='%(message)s')

# Start listening for keyboard inputs
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

"""
done = False
i = 10
q = queue.Queue()
made_determ = False
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
    _, _, _, _, info = env.step(action)
    
    if info["determinator"] == 121 and not made_determ: 
        #print(make_decision())
        print(f"Made decision{i}")
        action[8] = 1
        q.put(action)
        q.put(action)
        i = 1
        made_determ = True
    else:
        i = i + 1
        if q.empty():
            print("STOP IT NO MORE AI THINGS")
            made_determ = False
            
        else:
            _, _, _, _, info = env.step(q.get())
            print(f"Getting Queue{i}")
            if q.empty() and info["determinator"] == 121:
                print("Uh oh you got through the queue but determinator hasn't updated yet.")
            

    
listener.stop()
env.close()
print("Game loop exited.")"""

"""async def render_environment(env):
    #Task to render the environment and handle inputs.
    global keys_pressed, info, made_determ
    while not exit_flag[0]:
        # Render the game
        #if made_determ:
        #    await check_determinator
        print(f"determinator is {info["determinator"]}")
        env.render()

        # Update action array based on keys pressed
        action = [0] * 9
        for key in keys_pressed:
            action[key_to_action[key]] = 1
        
        # Perform the action in the environment
        _, _, done, _, info = env.step(action)

        # Stop if done
        if done:
            exit_flag[0] = True

        await asyncio.sleep(0.016) 

async def check_determinator(env):
    global info
    #global info, made_determ
    #Task to check info['determinator'] and make AI decisions.
    i = 10  # Cooldown logic
    while not exit_flag[0]:
        env.render()
        _, _, _, _, info = env.step([0] * 9)  # Fetch latest info

        if info.get("determinator") == 121:
            print(f"Made decision {i}")
            # Execute decision-making actions
            determ_action = [0] * 9
            determ_action[8] = 1  # Example decision: press 'A'
            #while(info.get("determinator") == 121):
            #    _, _, _, _, info = env.step(determ_action)
            #print("we pressed A!")
            _, _, _, _, info = env.step(determ_action)
            await asyncio.sleep(0.5)
            _, _, _, _, info = env.step(determ_action)
            await asyncio.sleep(0.5)

            i = 1
            #made_determ = True
        else:
            print("STOP IT NO MORE AI THINGS")
            i += 1
            #made_determ = False

        await asyncio.sleep(0.2)  # Adjust timing as needed

async def main(env):
    #Main function to run tasks concurrently.
    await asyncio.gather(
        render_environment(env),
        check_determinator(env)
    )

made_determ = False
_, _, done, _, info = env.step([0] * 9)
asyncio.run(main(env))"""

import asyncio
from collections import deque

action_queue = deque()
action_taken = False  # State variable to track if an action has been taken

async def render_environment(env):
    """Task to render the environment and handle inputs."""
    global keys_pressed
    while not exit_flag[0]:
        print("Render_env")
        #env.render()

        # Update action array based on keys pressed
        action = [0] * 9
        for key in keys_pressed:
            action[key_to_action[key]] = 1
        
        # Perform the action in the environment
        _, _, done, _, info = env.step(action)

        # Stop if done
        if done:
            exit_flag[0] = True

        await asyncio.sleep(1/60)  # Adjust as necessary

async def check_determinator(env):
    """Task to check info['determinator'] and make AI decisions."""
    global action_taken
    while not exit_flag[0]:
        _, _, _, _, info = env.step([0] * 9)  # Fetch latest info without doing any action
        
        if info.get("determinator") == 121 and not action_taken:
            print(f"Making decision based on determinator")
            action = [0] * 9
            action[8] = 1  # Example action: press 'A'
            action_queue.append(action)  # Queue the action
            action_queue.append(action)  # Queue the action
            action_taken = True  # Set action taken to True

            # Allow some time for the game to process the action
            await asyncio.sleep(3)  # Adjust this delay based on how long you need
            
        elif info.get("determinator") != 121:
            action_taken = False  # Reset action_taken when determinator changes

        await asyncio.sleep(0.1)  # Control how often to check

async def process_actions(env):
    """Task to process actions from the queue."""
    while not exit_flag[0]:
        while action_queue:  # Process all available actions
            #env.render()
            action = action_queue.popleft()  # Get the next action from the queue
            _, _, done, _, info = env.step(action)

            print(f'action taken{action}')
            await asyncio.sleep(3)  # Control the rate of processing actions

            if done:
                exit_flag[0] = True
                break
        await asyncio.sleep(1)  # Control the rate of processing actions    
        

async def main(env):
    """Main function to run tasks concurrently."""
    await asyncio.gather(
        render_environment(env),
        check_determinator(env),
        process_actions(env)
    )

asyncio.run(main(env))
