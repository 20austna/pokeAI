import retro
import retro.data  
from processText import process_move_menu_variables, process_text_box_variables, Decode, print_encoding_values
from pokemon import Pokemon
import logging
import asyncio


def menu_text_info():
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

done = False
i = 0

while not done:
    env.render()

    #update the action array based on keys pressed
    action = [0] * 9 # Reset actions

    # Perform the action in the environment
    obs, _, done, _, info = env.step(action)

    if info["determinator"] == 121 and i >= 10: 
        #print(make_decision())
        print(f"Made decision{i}")
        action[8] = 1
        obs, _, done, _, info = env.step(action)
        obs, _, done, _, info = env.step(action)
        i = 1
    else:
        print("STOP IT NO MORE AI THINGS")
        i = i + 1
