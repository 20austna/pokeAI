import retro
import retro.data  
import json
import struct
import sys
import logging
import time
import re  # For regex matching
from pynput import keyboard
from pokemon import Pokemon

def process_move_menu_variables(info):
    """
    Process the move_menu variables from the `info` dictionary. 

    Args:
        info (dict): Dictionary containing the game's RAM variables and their values.

    Returns:
        str: A single string representing the decoded move menu contents.
    """
    # List to hold the concatenated values for each move
    moves = []
    # List to hold tuples of (variable name, decoded value)
    #move_menu = []

    # Extract keys related to move_menu variables
    move_menu_keys = [key for key in info.keys() if re.match(r'move_menu_move_\d+_text\d+', key)]

    # Sort the keys by move number and text index
    def move_menu_sort_key(key):
        parts = key.split('_')
        move_num = int(parts[3])  # Extract move number (e.g., "move_menu_move_1") #move
        text_index = int(re.search(r'\d+', parts[4]).group())  # Extract numeric part of "textX"
        return (move_num, text_index)

    # Sort the keys in proper order
    sorted_keys = sorted(move_menu_keys, key=move_menu_sort_key)

    current_move = []
    current_move_num = None

    for key in sorted_keys:
        move_num = int(key.split('_')[3])  # Extract move number from the key
        if current_move_num is None or move_num == current_move_num:
            current_move.append(info[key])
        else:
        # Decode the current move and add it to the list
            moves.append(Decode(current_move))
            current_move = [info[key]]  # Start a new move
        current_move_num = move_num

    # Don't forget to decode the last move
    if current_move:
        moves.append(Decode(current_move))

    # Join moves with line breaks
    return "\n".join(moves)

    # Extract move_menu variables and their values in sorted order
    #for key in sorted_keys:
    #    move_menu.append(info[key])  # Append the value of the variable

    # Decode all values in order
    #decoded_text = Decode(move_menu)  # Decode the concatenated list of values
    #return decoded_text  # Return the decoded string



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

# useful for determining what to do with text box information
# print a list of all in game characters and their correponding Hex & Decmal values
def print_encoding_values():
    chart = create_encoding_chart()
    for row_index, row in enumerate(chart):
        for col_index, value in enumerate(row):
            if value and value != "Control characters":
                hex_value = f"{row_index:X}{col_index:X}"
                dec_value = int(hex_value, 16)
                if dec_value != 0:  # Ignore 0x00
                    print(f"Character: '{value}' | Hex: 0x{hex_value} | Decimal: {dec_value}")

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
"""
class Move:
    def __init__(self, name, move_type, power, accuracy, move_pp, attack_type, description):
        ""
        Initialize a new Move object.

        :param name: Name of the move (str)
        :param move_type: Type of the move (e.g., Fire, Water) (str)
        :param power: Power of the move (int)
        :param accuracy: Accuracy percentage of the move (int)
        :param move_pp: Maximum Power Points (PP) for the move (int)
        :param attack_type: Attack type (Physical or Special) (str)
        :param move_description: decsription of the move (str)S
        ""
        self.name = name
        self.move_type = move_type
        self.power = power
        self.accuracy = accuracy
        self.move_pp = move_pp
        self.attack_type = attack_type
        self.description = description

    def __str__(self):
        ""
        String representation of the Move object.
        ""
        return (f"Move(name={self.name}, type={self.move_type}, power={self.power}, "
                f"accuracy={self.accuracy}, PP={self.move_pp}, attack type={self.attack_type}, "
                f"description={self.move_description})")
"""