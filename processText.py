import re
# This function was originally only intended to deal with the move menu 
# But as it turns out we were able to get any text from the screen using this method
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

    # Extract keys related to move_menu variables
    move_menu_keys = [key for key in info.keys() if re.match(r'move_menu_move_\d+_text\d+', key)]

    # Sort the keys by move number and text index
    def move_menu_sort_key(key):
        parts = key.split('_')
        move_num = int(parts[3])  # Extract move number (e.g., "move_menu_move_1") 
        text_index = int(re.search(r'\d+', parts[4]).group())  # Extract numeric part of "textX"
        return (move_num, text_index)

    # Sort the keys in proper order
    sorted_keys = sorted(move_menu_keys, key=move_menu_sort_key)

    current_move = []
    current_move_num = None

    # Loop for decoding text in order of appearance
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


def Decode(decimal_values):
    """The text on screen is stored as decimal values in memory, so we need to decode these values"""
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
    # https://bulbapedia.bulbagarden.net/wiki/Character_encoding_(Generation_II)
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

# Useful for determining what to do with text box information
# print a list of all in game characters and their correponding Hex & Decmal values
def print_encoding_values():
    chart = create_encoding_chart()
    for row_index, row in enumerate(chart):
        for col_index, value in enumerate(row):
            if value and value != "Control characters":
                hex_value = f"{row_index:X}{col_index:X}"
                dec_value = int(hex_value, 16)
                if dec_value != 0:  
                    print(f"Character: '{value}' | Hex: 0x{hex_value} | Decimal: {dec_value}")