import retro
import retro.data  
import json
import struct
import sys
import logging
import time
import re  # For regex matching

def process_text_box_variables(info):
    # List to hold tuples of (textBox name, decoded value)
    text_boxes = []

    # Extract only the keys that correspond to textBox_X (numeric X)
    text_box_keys = [key for key in info.keys() if re.match(r'textBox_\d+', key)]

    # Sort the keys based on the numeric part (after 'textBox_')
    sorted_keys = sorted(text_box_keys, key=lambda x: int(x.split('_')[1]))

    # Extract textBox variables and their values from the sorted keys
    for key in sorted_keys:
        text_boxes.append((key, info[key]))  # Store the variable name and its value

    # Decode each textBox value and return the results as a list of decoded strings
    decoded_strings = []
    for _, text_box_value in text_boxes:
        decoded_text = Decode([text_box_value])  # Decode each text box value
        decoded_strings.append(decoded_text)

    return decoded_strings  # Return a list of decoded textBox strings

def Decode(decimal_values):
    # Get the encoding chart
    chart = create_encoding_chart()
    
    # Initialize an empty string to store the decoded characters
    decoded_string = ""
    
    # Process each decimal value in the array
    for dec_value in decimal_values:
        # Convert the decimal value to a hexadecimal string
        hex_value = f"{dec_value:X}"
        
        # Split the hexadecimal value into row and column indices
        if len(hex_value) == 2:  # Hex value has 2 characters (1 byte address)
            row_index = int(hex_value[0], 16)
            col_index = int(hex_value[1], 16)
        else:
            continue  # Ignore invalid values
        
        # Check if the row and column indices are within the bounds of the chart
        if row_index < len(chart) and col_index < len(chart[row_index]):
            char = chart[row_index][col_index]
            if char and char != "Control characters":  # Only add valid characters
                decoded_string += char

    return decoded_string

def create_encoding_chart():
    #https://bulbapedia.bulbagarden.net/wiki/Character_encoding_(Generation_II)
    chart = [
        ["?", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"],
        ["Q", "R", "S", "T", "", "X", "Y", "Z", "(", ")", ":", ";", "[", "", "", ""],
        ["q", "r", "", "", "w", "x", "y", "z", "", "", "", "", "", "", "", ""],
        ["Ä", "Ö", "Ü", "ä", "ö", "", "", "", "", "", "", "", "", "", "", ""],
        ["Z", "(", ")", ":", "", "", "", "", "", "", "", "", "'r", "", "", ""],
        ["Control characters"],
        ["█", "▲", "🖁", "D", "E", "F", "G", "H", "I", "V", "S", "L", "M", ":", "ぃ", "ぅ"],
        ["PO", "Ké", "“", "”", "・", "…", "ぁ", "ぇ", "ぉ", "╔", "═", "╗", "║", "╚", "╝", " "],
        ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"],
        ["Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "(", ")", ":", ";", "[", "]"],
        ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"],
        ["q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "", "", "", "", "", ""],
        ["Ä", "Ö", "Ü", "ä", "ö", "ü", "", "", "", "", "", "", "", "", "", ""],
        ["'d", "'l", "'m", "'r", "'s", "'t", "'v", "", "", "", "", "", "", "", "", "🡄"],
        ["'", "PK", "MN", "-", "", "", "?", "!", ".", "&", "é", "🡆", "▷", "▶", "▼", "♂"],
        ["Poké Dollar", "×", ".", "/", ",", "♀", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    ]
    return chart

def print_encoding_values():
    chart = create_encoding_chart()
    for row_index, row in enumerate(chart):
        for col_index, value in enumerate(row):
            if value and value != "Control characters":
                hex_value = f"{row_index:X}{col_index:X}"
                dec_value = int(hex_value, 16)
                if dec_value != 0:  # Ignore 0x00
                    print(f"Character: '{value}' | Hex: 0x{hex_value} | Decimal: {dec_value}")

# Run the function
print_encoding_values()


# TODO create and test a variable in the data.json track the number of moves each pokemon in our party has 
# TODO create and test a varible in the data.json to track the number of pokemon in our party
# https://datacrystal.tcrf.net/wiki/Pok%C3%A9mon_Gold_and_Silver/RAM_map
# TODO create party class(consists of numPokemon Pokemon)
# TODO create pokemon class(consists of a pokemon with numMoves moves and all the pokemon's stats)
# TODO further investigate using bulbapedia API
# https://bulbapedia.bulbagarden.net/wiki/Special:ApiSandbox
# https://www.mediawiki.org/wiki/API:Main_page
# TODO create hardcoded type chart
# TODO create method makeDecision(info) which returns a decision
# this should be a move but in future we'll incorperate a switch and an item. 
# TODO create method completeDecision(decision, info) which returns a list of action arrays to accomplish the task
# in the future the second parameter will only contain text box info. That way it can tell where the cursor is pointed. 
# but first i need to figure out various text boxes. 
# TODO moves class
# TODO how does chat gpt call information from classes we have -- issue made

game='PokemonSilver-GbColor'
data_path = "/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor/data.json"
scenario_path = "/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor/scenario.json"
env = retro.make(game, 'Battle.state') #in the Battle.state file we have 1 pokemon, Totodile, which is our current pokemon. 
env.reset()

done = False
i = 0
print(env.buttons)

logging.basicConfig(filename='info_log.txt', level=logging.INFO, format='%(message)s')


done = False
i = 0
action = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # Default action with no buttons pressed
action[4] = 1  # Press A
obs, _, done, _, info = env.step(action)
decoded_texts = process_text_box_variables(info)

# Combine the decoded texts into a single string (if desired)
combined_text = ''.join(decoded_texts)
print(f"Decoded Text: {combined_text}")
action[4] = 0  # Press UP
action[8] = 1  # Press A
env.render()
obs, _, done, _, info = env.step(action)
# main loop
while not done:
    env.render() # render the game
    action = [0,0,0,0,0,0,0,0,0] # all controller inputs are set to off, try print(env.buttons) for more info

    # every time we do env.step we step forward a frame in the game. 
    # during this frame we can pass in controller input via the action[] array
    obs, _, done, _, info = env.step(action) 
    # after performing this action we get back some information from the games' RAM 
    # this is stored in the variables on the left. 
    # since this isnt a traditional reinforcement learning project we dont need to keep track rewards.
    # what we really care about is is the info dictionary 
    # which contains the names of variables from data.json file and the values at their memory addresses in RAM

    # Step 2: Continue for 60 iterations after pressing "A" with no further inputs
    if i > 0 and i <= 300:
        action = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # No further inputs
    elif i == 301:
        # Step 3: After 60 iterations, log the info
        logging.info(f"Captured info at step {i}: {info}")
        
        # Step 4: Process the textBox values in order using the process_text_box_variables function
        decoded_texts = process_text_box_variables(info)

        # Combine the decoded texts into a single string (if desired)
        combined_text = ''.join(decoded_texts)

        print(f"Decoded Text: {combined_text}")
        done = True  # Stop after capturing info and printing decoded text

    i += 1
    #time.sleep(0.1)  # Optional delay for smoother iteration, can be adjusted

#textBox_9 is also where the arrow/space next to fight is
#textBox_15 is also where the arrow/space next to 