import re
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

def Decode(decimal_values):
    # Get the encoding chart
    chart = create_encoding_chart()

    # Control characters and their descriptions
    control_character_descriptions = {
        76: "Autoscroll: Scrolls the standard text window up one line without player confirmation.",
        78: "Double-spaced line break: Moves print position two tiles below the current line.",
        79: "Second line: Moves print position to the start of the second line.",
        80: "String terminator: Ends the string. Often pads shorter strings.",
        81: "Paragraph: Clears text window after confirmation, then starts printing in a new window.",
    }
    
    # Initialize an empty string to store the decoded characters
    decoded_string = ""
    
    # Process each decimal value in the array
    for dec_value in decimal_values:

        if dec_value in control_character_descriptions:
            # Add a descriptive placeholder for the control character
            decoded_string += f"[{control_character_descriptions[dec_value]}]"
            # Trigger potential actions based on specific control characters
            if dec_value in {76, 81}:  # Examples where AI might be called
                trigger_ai_call(dec_value)
            continue

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

def trigger_ai_call(control_char):
    """Placeholder function to trigger AI interaction based on control characters."""
    # Add custom logic to call the AI decision-making module here
    print(f"AI triggered by control character: {control_char}")

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
