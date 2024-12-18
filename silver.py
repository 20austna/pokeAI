import retro
import retro.data  
import logging
import asyncio
from collections import deque
from action_ai import get_action_queue
from processText import process_move_menu_variables, Decode, print_encoding_values
from pynput import keyboard
from pokemon import Pokemon
from decision_ai import make_decision
from functools import partial

# To find more RAM address to add to the data.json follow the link below. 
# https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Gold_and_Silver/RAM_map

# Logging function for game info
def log_game_info(shared_state):
    info = shared_state.get("info", {})
    logging.info(f"Captured info: {info}")
    print(f"Captured info: {info}")

def menu_text_info(shared_state):
        info = shared_state.get("info", {})
        decoded_menu_text = process_move_menu_variables(info)
        print(f"\n{decoded_menu_text}")

# Set up logging for game info
logging.basicConfig(filename='info_log.txt', level=logging.INFO, format='%(message)s')

game='PokemonSilver-GbColor'
# Make sure to change 
data_path = "/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor/data.json" 
scenario_path = "/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor/scenario.json"
env = retro.make(game, 'rivalBattle.state')
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

action_queue = deque()

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
        # Update action array based on keys pressed
        action = [0] * 9
        for key in shared_state["keys_pressed"]:
            action[key_to_action[key]] = 1
        
        # Perform the action in the environment
        _, _, done, _, shared_state["info"] = env.step(action)

        # Stop if done
        if done:
            shared_state["exit_flag"] = True

        await asyncio.sleep(1/60)  


def create_pokemon(info): 
    """Create a pokemon object from memory values inside of data.json"""
    move_1 = {
        "id":info.get("Current_Move_1"),
        "current_move_pp":info.get("Current_Move_1_PP")
    }
    move_2 = {
        "id":info.get("Current_Move_2"),
        "current_move_pp":info.get("Current_Move_2_PP")
    }
    move_3 = {
        "id":info.get("Current_Move_3"),
        "current_move_pp":info.get("Current_Move_3_PP")
    }
    move_4 = {
        "id":info.get("Current_Move_4"),
        "current_move_pp":info.get("Current_Move_4_PP")
    }
    our_current_mon = Pokemon(
        id=info.get("Current_Mon"),
        moves = [move_1, move_2, move_3, move_4],
        hp=info.get("Mon_1_HP_2"),
        attack=info.get("Mon_1_Attack_2"),
        defense=info.get("Mon_1_Defense_2"),
        special_attack=info.get("Mon_1_Sp_Attack_2"),
        special_defense=info.get("Mon_1_Sp_Defense_2"),
        speed=info.get("Mon_1_Speed_2")
    )

    their_current_mon = Pokemon(
        id=info.get("Their_Current_Mon"),
        hp=info.get("Mon_1_HP_2")
    )
    
    return our_current_mon, their_current_mon

def print_action_taken(action):
    """
    Prints which button on the controller is being pressed based on the action array.
    
    Args:
    action (list): A list of integers where 1 indicates a button press and 0 indicates no press.
                   Only one element in the list will be 1 at a time.
    """
    # Reverse the key_to_action dictionary to map indices to keys
    action_to_key = {v: k for k, v in key_to_action.items()}
    button_labels = {
        'z': 'B',
        'tab': 'SELECT',
        'enter': 'START',
        'up': 'UP',
        'down': 'DOWN',
        'left': 'LEFT',
        'right': 'RIGHT',
        'x': 'A'
    }
    
    try:
        # Find the index of the pressed button
        pressed_index = action.index(1)
        key = action_to_key.get(pressed_index, None)
        if key:
            print(f"Button pressed: {button_labels[key]}")
        else:
            print("Unknown button pressed.")
    except ValueError:
        print("No button is pressed.")

async def check_determinator(env, shared_state):
    """Task to check info['determinator'] and make AI decisions."""
    # Shared states to keep track of if an action has been taken in the main menu or the move menu
    action_taken = shared_state["action_taken"] 
    move_taken = shared_state["move_taken"] 
    decision_string = None

    while not shared_state["exit_flag"]:
        await asyncio.sleep(1.3) # Let menus load
        _, _, _, _, shared_state["info"] = env.step([0] * 9)  # Fetch latest info without doing any action
        
        action_taken = shared_state["action_taken"]
        move_taken = shared_state["move_taken"]
        info = shared_state["info"] 

        # If we see that a specific character in a specific place on screen we know we're in the main menu
        if info and info.get("determinator") == 121 and not action_taken and not move_taken:
            menu_str = process_move_menu_variables(info) # Get the text on screen
            print(f"Menu state:\n{menu_str}")
            pokemon=create_pokemon(info)
            decision_string = make_decision(pokemon[0], pokemon[1])
            print(f"Decision AI Reasoning: {decision_string}")
            action = [0] * 9 # Create an action array with none of the controller inputs set to true
            shared_state["action_taken"] = True
            action_arr = get_action_queue(decision_string, menu_str) # Function returns an array

            for actions in action_arr:
                action[actions] = 1 # Each number in the action_arr corresponds to a single button on the controller we want to press 
                action_queue.append(action) # Appends it to a queue that is proccessed inside of process_actions(env, shared_state)
                action = [0] * 9 
        
            await asyncio.sleep(3) # Allow some time for the game to process the action
        
        # If we see a specific character in a specific place on screen we know we're in the move menu
        elif info and info.get("move_determinator") == 126 and info.get("determinator") != 121 and not move_taken:
            # This code is all essentially the same as the block above except for the "if"
            menu_str = process_move_menu_variables(info)
            print(f"Menu state\n{menu_str}")
            if not decision_string: # Make sure we aren't asking the decision AI to pick a move if we're already picked one
                print(f"Making decision based on move determinator. \n Menu state\n{menu_str}")
                pokemon=create_pokemon(info)
                decision_string = make_decision(pokemon[0], pokemon[1])
                print(f"Decision: {decision_string}")
            action = [0] * 9
            shared_state["move_taken"] = True
            action_arr = get_action_queue(decision_string, menu_str)
            for actions in action_arr: 
                action[actions] = 1
                action_queue.append(action)
                action = [0] * 9 

            # Allow some time for the game to process the action
            await asyncio.sleep(3) 

        await asyncio.sleep(0.1)  # Control how often to check

async def process_actions(env, shared_state):
    """Task to process actions from the queue."""
    while not shared_state["exit_flag"]:
        action_taken = shared_state["action_taken"]
        move_taken = shared_state["move_taken"]
        while action_queue:  # Process all available actions
            action = action_queue.popleft()  # Get the next action from the queue
            _, _, done, _, shared_state["info"] = env.step(action)

            print_action_taken(action)
            await asyncio.sleep(1)  # Control the rate of processing actions
        
            if done:
                shared_state["exit_flag"] = True
                break
        if action_taken:
            shared_state["action_taken"] = False
        if move_taken:
            shared_state["move_taken"] = False

        await asyncio.sleep(1)  # Control the rate of processing actions    
        

async def main(env):
    """Main function to run tasks concurrently."""
    await asyncio.gather(
        render_environment(env,shared_state),
        check_determinator(env,shared_state),
        process_actions(env, shared_state)
    )

asyncio.run(main(env))