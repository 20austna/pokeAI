import retro
import retro.data  
import json
import struct
import sys
import logging
import time
import re  # For regex matching

pokemon_dict =  {0: '?????', 1: 'Bulbasaur', 2: 'Ivysaur', 3: 'Venusaur', 4: 'Charmander', 
                 5: 'Charmeleon', 6: 'Charizard', 7: 'Squirtle', 8: 'Wartortle', 9: 'Blastoise', 
                 10: 'Caterpie', 11: 'Metapod', 12: 'Butterfree', 13: 'Weedle', 14: 'Kakuna', 
                 15: 'Beedrill', 16: 'Pidgey', 17: 'Pidgeotto', 18: 'Pidgeot', 19: 'Rattata', 
                 20: 'Raticate', 21: 'Spearow', 22: 'Fearow', 23: 'Ekans', 24: 'Arbok', 
                 25: 'Pikachu', 26: 'Raichu', 27: 'Sandshrew', 28: 'Sandslash', 29: 'Nidoran♀', 
                 30: 'Nidorina', 31: 'Nidoqueen', 32: 'Nidoran♂', 33: 'Nidorino', 34: 'Nidoking', 
                 35: 'Clefairy', 36: 'Clefable', 37: 'Vulpix', 38: 'Ninetales', 39: 'Jigglypuff', 
                 40: 'Wigglytuff', 41: 'Zubat', 42: 'Golbat', 43: 'Oddish', 44: 'Gloom', 
                 45: 'Vileplume', 46: 'Paras', 47: 'Parasect', 48: 'Venonat', 49: 'Venomoth', 
                 50: 'Diglett', 51: 'Dugtrio', 52: 'Meowth', 53: 'Persian', 54: 'Psyduck', 
                 55: 'Golduck', 56: 'Mankey', 57: 'Primeape', 58: 'Growlithe', 59: 'Arcanine', 
                 60: 'Poliwag', 61: 'Poliwhirl', 62: 'Poliwrath', 63: 'Abra', 64: 'Kadabra', 
                 65: 'Alakazam', 66: 'Machop', 67: 'Machoke', 68: 'Machamp', 69: 'Bellsprout', 
                 70: 'Weepinbell', 71: 'Victreebel', 72: 'Tentacool', 73: 'Tentacruel', 74: 'Geodude', 
                 75: 'Graveler', 76: 'Golem', 77: 'Ponyta', 78: 'Rapidash', 79: 'Slowpoke', 
                 80: 'Slowbro', 81: 'Magnemite', 82: 'Magneton', 83: "Farfetch'd", 84: 'Doduo', 
                 85: 'Dodrio', 86: 'Seel', 87: 'Dewgong', 88: 'Grimer', 89: 'Muk', 
                 90: 'Shellder', 91: 'Cloyster', 92: 'Gastly', 93: 'Haunter', 94: 'Gengar', 
                 95: 'Onix', 96: 'Drowzee', 97: 'Hypno', 98: 'Krabby', 99: 'Kingler', 
                 100: 'Voltorb', 101: 'Electrode', 102: 'Exeggcute', 103: 'Exeggutor', 104: 'Cubone', 
                 105: 'Marowak', 106: 'Hitmonlee', 107: 'Hitmonchan', 108: 'Lickitung', 109: 'Koffing', 
                 110: 'Weezing', 111: 'Rhyhorn', 112: 'Rhydon', 113: 'Chansey', 114: 'Tangela', 
                 115: 'Kangaskhan', 116: 'Horsea', 117: 'Seadra', 118: 'Goldeen', 119: 'Seaking', 
                 120: 'Staryu', 121: 'Starmie', 122: 'Mr. Mime', 123: 'Scyther', 124: 'Jynx', 
                 125: 'Electabuzz', 126: 'Magmar', 127: 'Pinsir', 128: 'Tauros', 129: 'Magikarp', 
                 130: 'Gyarados', 131: 'Lapras', 132: 'Ditto', 133: 'Eevee', 134: 'Vaporeon', 
                 135: 'Jolteon', 136: 'Flareon', 137: 'Porygon', 138: 'Omanyte', 139: 'Omastar', 
                 140: 'Kabuto', 141: 'Kabutops', 142: 'Aerodactyl', 143: 'Snorlax', 144: 'Articuno', 
                 145: 'Zapdos', 146: 'Moltres', 147: 'Dratini', 148: 'Dragonair', 149: 'Dragonite', 
                 150: 'Mewtwo', 151: 'Mew', 152: 'Chikorita', 153: 'Bayleef', 154: 'Meganium', 
                 155: 'Cyndaquil', 156: 'Quilava', 157: 'Typhlosion', 158: 'Totodile', 159: 'Croconaw', 
                 160: 'Feraligatr', 161: 'Sentret', 162: 'Furret', 163: 'Hoothoot', 164: 'Noctowl', 
                 165: 'Ledyba', 166: 'Ledian', 167: 'Spinarak', 168: 'Ariados', 169: 'Crobat', 
                 170: 'Chinchou', 171: 'Lanturn', 172: 'Pichu', 173: 'Cleffa', 174: 'Igglybuff', 
                 175: 'Togepi', 176: 'Togetic', 177: 'Natu', 178: 'Xatu', 179: 'Mareep', 
                 180: 'Flaaffy', 181: 'Ampharos', 182: 'Bellossom', 183: 'Marill', 184: 'Azumarill', 
                 185: 'Sudowoodo', 186: 'Politoed', 187: 'Hoppip', 188: 'Skiploom', 189: 'Jumpluff', 
                 190: 'Aipom', 191: 'Sunkern', 192: 'Sunflora', 193: 'Yanma', 194: 'Wooper', 
                 195: 'Quagsire', 196: 'Espeon', 197: 'Umbreon', 198: 'Murkrow', 199: 'Slowking', 
                 200: 'Misdreavus', 201: 'Unown', 202: 'Wobbuffet', 203: 'Girafarig', 204: 'Pineco', 
                 205: 'Forretress', 206: 'Dunsparce', 207: 'Gligar', 208: 'Steelix', 209: 'Snubbull', 
                 210: 'Granbull', 211: 'Qwilfish', 212: 'Scizor', 213: 'Shuckle', 214: 'Heracross', 
                 215: 'Sneasel', 216: 'Teddiursa', 217: 'Ursaring', 218: 'Slugma', 219: 'Magcargo', 
                 220: 'Swinub', 221: 'Piloswine', 222: 'Corsola', 223: 'Remoraid', 224: 'Octillery', 
                 225: 'Delibird', 226: 'Mantine', 227: 'Skarmory', 228: 'Houndour',  229: 'Houndoom', 
                 230: 'Kingdra', 231: 'Phanpy', 232: 'Donphan', 233: 'Porygon2', 234: 'Stantler', 
                 235: 'Smeargle', 236: 'Tyrogue', 237: 'Hitmontop', 238: 'Smoochum', 239: 'Elekid', 
                 240: 'Magby', 241: 'Miltank', 242: 'Blissey', 243: 'Raikou', 244: 'Entei', 
                 245: 'Suicune', 246: 'Larvitar', 247: 'Pupitar', 248: 'Tyranitar', 249: 'Lugia', 
                 250: 'Ho-Oh', 251: 'Celebi', 252: '?????', 253: 'Egg', 254: '?????', 255: '?????'}

move_dict =  {0: '[glitchy]', 1: 'Pound', 2: 'Karate Chop', 3: 'Doubleslap', 4: 'Comet Punch', 
              5: 'Mega Punch', 6: 'Pay Day', 7: 'Fire Punch', 8: 'Ice Punch', 9: 'Thunderpunch', 
              10: 'Scratch', 11: 'Vicegrip', 12: 'Guillotine', 13: 'Razor Wind', 14: 'Swords Dance', 
              15: 'Cut', 16: 'Gust', 17: 'Wing Attack', 18: 'Whirlwind', 19: 'Fly', 
              20: 'Bind', 21: 'Slam', 22: 'Vine Whip', 23: 'Stomp', 24: 'Double Kick', 
              25: 'Mega Kick', 26: 'Jump Kick', 27: 'Rolling Kick', 28: 'Sand Attack', 29: 'Headbutt', 
              30: 'Horn Attack', 31: 'Fury Attack', 32: 'Horn Drill', 33: 'Tackle', 34: 'Body Slam', 
              35: 'Wrap', 36: 'Take Down', 37: 'Thrash', 38: 'Double-Edge', 39: 'Tail Whip', 
              40: 'Poison Sting', 41: 'Twineedle', 42: 'Pin Missile', 43: 'Leer', 44: 'Bite', 
              45: 'Growl', 46: 'Roar', 47: 'Sing', 48: 'Supersonic', 49: 'Sonicboom', 
              50: 'Disable', 51: 'Acid', 52: 'Ember', 53: 'Flamethrower', 54: 'Mist', 
              55: 'Water Gun', 56: 'Hydro Pump', 57: 'Surf', 58: 'Ice Beam', 59: 'Blizzard', 
              60: 'Psybeam', 61: 'Bubblebeam', 62: 'Aurora Beam', 63: 'Hyper Beam', 64: 'Peck', 
              65: 'Drill Peck', 66: 'Submission', 67: 'Low Kick', 68: 'Counter', 69: 'Seismic Toss', 
              70: 'Strength', 71: 'Absorb', 72: 'Mega Drain', 73: 'Leech Seed', 74: 'Growth', 
              75: 'Razor Leaf', 76: 'Solar Beam', 77: 'Poisonpowder', 78: 'Stun Spore', 79: 'Sleep Powder', 
              80: 'Petal Dance', 81: 'String Shot', 82: 'Dragon Rage', 83: 'Fire Spin', 84: 'Thundershock', 
              85: 'Thunderbolt', 86: 'Thunder Wave', 87: 'Thunder', 88: 'Rock Throw', 89: 'Earthquake', 
              90: 'Fissure', 91: 'Dig', 92: 'Toxic', 93: 'Confusion', 94: 'Psychic', 
              95: 'Hypnosis', 96: 'Meditate', 97: 'Agility', 98: 'Quick Attack', 99: 'Rage', 
              100: 'Teleport', 101: 'Night Shade', 102: 'Mimic', 103: 'Screech', 104: 'Double Team', 
              105: 'Recover', 106: 'Harden', 107: 'Minimize', 108: 'Smokescreen', 109: 'Confuse Ray', 
              110: 'Withdraw', 111: 'Defense Curl', 112: 'Barrier', 113: 'Light Screen', 114: 'Haze', 
              115: 'Reflect', 116: 'Focus Energy', 117: 'Bide', 118: 'Metronome', 119: 'Mirror Move', 
              120: 'Selfdestruct', 121: 'Egg Bomb', 122: 'Lick', 123: 'Smog', 124: 'Sludge', 
              125: 'Bone Club', 126: 'Fire Blast', 127: 'Waterfall', 128: 'Clamp', 129: 'Swift', 
              130: 'Skull Bash', 131: 'Spike Cannon', 132: 'Constrict', 133: 'Amnesia', 134: 'Kinesis', 
              135: 'Softboiled', 136: 'Hi Jump Kick', 137: 'Glare', 138: 'Dream Eater', 139: 'Poison Gas', 
              140: 'Barrage', 141: 'Leech Life', 142: 'Lovely Kiss', 143: 'Sky Attack', 144: 'Transform', 
              145: 'Bubble', 146: 'Dizzy Punch', 147: 'Spore', 148: 'Flash', 149: 'Psywave', 
              150: 'Splash', 151: 'Acid Armor', 152: 'Crabhammer', 153: 'Explosion', 154: 'Fury Swipes', 
              155: 'Bonemerang', 156: 'Rest', 157: 'Rock Slide', 158: 'Hyper Fang', 159: 'Sharpen', 
              160: 'Conversion', 161: 'Tri Attack', 162: 'Super Fang', 163: 'Slash', 164: 'Substitute', 
              165: 'Struggle', 166: 'Sketch', 167: 'Triple Kick', 168: 'Thief', 169: 'Spider Web', 
              170: 'Mind Reader', 171: 'Nightmare', 172: 'Flame Wheel', 173: 'Stnore', 174: 'Curse', 
              175: 'Flail', 176: 'Conversion2', 177: 'Aeroblast', 178: 'Cotton Spore', 179: 'Reversal', 
              180: 'Spite', 181: 'Powder Snow', 182: 'Protect', 183: 'Mach Punch', 184: 'Scary Face', 
              185: 'Faint Attack', 186: 'Sweet Kiss', 187: 'Belly Drum', 188: 'Sludge Bomb', 189: 'Mud-Slap', 
              190: 'Octazooka', 191: 'Spikes', 192: 'Zap Cannon', 193: 'Foresight', 194: 'Destiny Bond', 
              195: 'Perish Song', 196: 'Icy Wind', 197: 'Detect', 198: 'Bone Rush', 199: 'Lock-On', 
              200: 'Outrage', 201: 'Sandstorm', 202: 'Giga Drain', 203: 'Endure', 204: 'Charm', 
              205: 'Rollout', 206: 'False Swipe', 207: 'Swagger', 208: 'Milk Drink', 209: 'Spark', 
              210: 'Fury Cutter', 211: 'Steel Wing', 212: 'Mean Look', 213: 'Attract', 214: 'Sleep Talk', 
              215: 'Heal Bell', 216: 'Return', 217: 'Present', 218: 'Frustration', 219: 'Safeguard', 
              220: 'Pain Split', 221: 'Sacred Fire', 222: 'Magnitude', 223: 'Dynamicpunch', 224: 'Megahorn', 
              225: 'Dragonbreath', 226: 'Baton Pass', 227: 'Encore', 228: 'Pursuit', 229: 'Rapid Spin', 
              230: 'Sweet Scent', 231: 'Iron Tail', 232: 'Metal Claw', 233: 'Vital Throw', 234: 'Morning Sun', 
              235: 'Synthesis', 236: 'Moonlight', 237: 'Hidden Power', 238: 'Cross Chop', 239: 'Twister', 
              240: 'Rain Dance', 241: 'Sunny Day', 242: 'Crunch', 243: 'Mirror Coat', 244: 'Psych Up', 
              245: 'Extremespeed', 246: 'Ancientpower', 247: 'Shadow Ball', 248: 'Future Sight', 249: 'Rock Smash', 
              250: 'Whirlpool', 251: 'Beat Up', 252: '[blank]', 253: '999ZAA', 254: '[glitchy]', 255: '[glitchy]'}

def find_poke_name(pokemon_id):
    """
    Given a pokemon ID, return the corresponding Pokemon name from the pokemon_dict.
    """
    return pokemon_dict.get(pokemon_id, "Unknown Pokémon")

def find_move_name(move_id):
    """
    Given a move ID, return the corresponding move name from the move_dict.
    """
    return move_dict.get(move_id, "Unknown Move")

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

  '''
class Pokemon:
    def __init__(self, pokemon_id, move_1, move_2, type_1, type_2=None, level, hp, defense, attack, ability):
        self.name = find_poke_name(pokemon_id)
        self.move1 = move_1
        self.move2 = move_2
        self.type1 = type_1
        self.type2 = type_2
        self.level = level
        self.hp = hp
        self.defense = defense
        self.attack = attack
        self.ability = ability
        
vhagar = Pokemon(
    pokemon_id=150, #Mewtwo
    move_1 = "Dracrys",
    move_2 = "Sneak Attack",
    type_1 = "Dragon",
    type_2 = "Fire",
    Level = 100,
    hp = 120,
    defense = 100,
    attack = 150,
    ability = "Fire Breath"
)

        
'''

#textBox_9 is also where the arrow/space next to fight is
#textBox_15 is also where the arrow/space next to 
