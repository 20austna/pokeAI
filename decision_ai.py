"""def make_decision(our_pokemon, opponent_pokemon, menu_state):
    
    
    #This will serve as an AI decision-making function in order to decide what the best move 
    #would be during in a Pokemon battle.
    
    #Args:
    #    our_pokemon: our own pokemon object.
    #    opponent_pokemon: opponent's pokemon object.
    #    menu_state (str): current menu state (ex: "Fight").
    
    #Returns:
    #    str: the best move to use.
    
    
    # we want to make sure we are in fight mode. if we aren't, then
    # no decision will be made
    if menu_state != "Fight":
        print("Not in the Fight menu so no decision made.")
        return None
    
    # simple debug statements
    print(f"Opponent HP: {opponent_pokemon.current_HP}/{opponent_pokemon.max_HP}")
    print(f"Opponent Level: {opponent_pokemon.level}")
    
    # filter out any moves that have 0 pp
    available_moves = [move for move in our_pokemon.moves if move["move_pp"] > 0]
    # if ALL our moves have no pp left than use struggle
    if not available_moves:
        print("No available moves left! Struggle must be used.")
        return "Struggle"
    
    # determine what the best move is based on effectiveness and power
    best_move = None
    # this variable will serve to track what the most effective move is
    best_score = -1 
    
    for move in available_moves:
        # get move stats
        move_name = move["name"]
        move_type = move["move_type"]
        move_power = move["power"]
        move_pp = move["move_pp"]
        
        # calculate the type effectiveness 
        # (if we do not know what the type is then use a default value of 1.0)
        effectiveness = type_effectiveness(move_type, opponent_pokemon.type1)
        if opponent_pokemon.type2:
            effectiveness = max(effectiveness, type_effectiveness(move_type, opponent_pokemon.type2))
        
        # calculate a score based on power and effectiveness which is the damage multiplier
        score = move_power * effectiveness
        if score > best_score:
            best_score = score
            best_move = move_name
    
    print(f"AI selected move: {best_move}")
    return best_move
    """


type_chart = {
    # fire type
    ("Fire", "Grass"): 2.0, ("Fire", "Bug"): 2.0, ("Fire", "Ice"): 2.0, ("Fire", "Steel"): 2.0,
    ("Fire", "Water"): 0.5, ("Fire", "Fire"): 0.5, ("Fire", "Rock"): 0.5, ("Fire", "Dragon"): 0.5,
    
    # water type
    ("Water", "Fire"): 2.0, ("Water", "Ground"): 2.0, ("Water", "Rock"): 2.0,
    ("Water", "Water"): 0.5, ("Water", "Grass"): 0.5, ("Water", "Dragon"): 0.5,
    
    # grass type
    ("Grass", "Water"): 2.0, ("Grass", "Ground"): 2.0, ("Grass", "Rock"): 2.0,
    ("Grass", "Fire"): 0.5, ("Grass", "Grass"): 0.5, ("Grass", "Poison"): 0.5,
    ("Grass", "Flying"): 0.5, ("Grass", "Bug"): 0.5, ("Grass", "Dragon"): 0.5, ("Grass", "Steel"): 0.5,
    
    # electric type
    ("Electric", "Water"): 2.0, ("Electric", "Flying"): 2.0,
    ("Electric", "Electric"): 0.5, ("Electric", "Grass"): 0.5, ("Electric", "Dragon"): 0.5,
    ("Electric", "Ground"): 0.0,
    
    # ice type
    ("Ice", "Grass"): 2.0, ("Ice", "Ground"): 2.0, ("Ice", "Flying"): 2.0, ("Ice", "Dragon"): 2.0,
    ("Ice", "Fire"): 0.5, ("Ice", "Water"): 0.5, ("Ice", "Ice"): 0.5, ("Ice", "Steel"): 0.5,
    
    # fighting type
    ("Fighting", "Normal"): 2.0, ("Fighting", "Ice"): 2.0, ("Fighting", "Rock"): 2.0, ("Fighting", "Dark"): 2.0,
    ("Fighting", "Steel"): 2.0,
    ("Fighting", "Poison"): 0.5, ("Fighting", "Flying"): 0.5, ("Fighting", "Psychic"): 0.5, ("Fighting", "Bug"): 0.5,
    ("Fighting", "Fairy"): 0.5, ("Fighting", "Ghost"): 0.0,
    
    # poison type
    ("Poison", "Grass"): 2.0, ("Poison", "Fairy"): 2.0,
    ("Poison", "Poison"): 0.5, ("Poison", "Ground"): 0.5, ("Poison", "Rock"): 0.5, ("Poison", "Ghost"): 0.5,
    ("Poison", "Steel"): 0.0,
    
    # ground type
    ("Ground", "Fire"): 2.0, ("Ground", "Electric"): 2.0, ("Ground", "Poison"): 2.0, ("Ground", "Rock"): 2.0,
    ("Ground", "Steel"): 2.0,
    ("Ground", "Grass"): 0.5, ("Ground", "Bug"): 0.5, ("Ground", "Flying"): 0.0,
    
    # flying type
    ("Flying", "Grass"): 2.0, ("Flying", "Fighting"): 2.0, ("Flying", "Bug"): 2.0,
    ("Flying", "Electric"): 0.5, ("Flying", "Rock"): 0.5, ("Flying", "Steel"): 0.5,
    
    # psychic type
    ("Psychic", "Fighting"): 2.0, ("Psychic", "Poison"): 2.0,
    ("Psychic", "Psychic"): 0.5, ("Psychic", "Steel"): 0.5, ("Psychic", "Dark"): 0.0,
    
    # bug type
    ("Bug", "Grass"): 2.0, ("Bug", "Psychic"): 2.0, ("Bug", "Dark"): 2.0,
    ("Bug", "Fire"): 0.5, ("Bug", "Fighting"): 0.5, ("Bug", "Poison"): 0.5, ("Bug", "Flying"): 0.5,
    ("Bug", "Ghost"): 0.5, ("Bug", "Steel"): 0.5, ("Bug", "Fairy"): 0.5,
    
    # rock type
    ("Rock", "Fire"): 2.0, ("Rock", "Ice"): 2.0, ("Rock", "Flying"): 2.0, ("Rock", "Bug"): 2.0,
    ("Rock", "Fighting"): 0.5, ("Rock", "Ground"): 0.5, ("Rock", "Steel"): 0.5,
    
    # ghost type
    ("Ghost", "Psychic"): 2.0, ("Ghost", "Ghost"): 2.0,
    ("Ghost", "Dark"): 0.5, ("Ghost", "Normal"): 0.0,
    ("Ghost", "Fairy"): 0.5,
    
    # dragon type
    ("Dragon", "Dragon"): 2.0,
    ("Dragon", "Steel"): 0.5, ("Dragon", "Fairy"): 0.0,
    
    # dark type
    ("Dark", "Psychic"): 2.0, ("Dark", "Ghost"): 2.0,
    ("Dark", "Fighting"): 0.5, ("Dark", "Dark"): 0.5, ("Dark", "Fairy"): 0.5,
    
    # steel type
    ("Steel", "Ice"): 2.0, ("Steel", "Rock"): 2.0, ("Steel", "Fairy"): 2.0,
    ("Steel", "Fire"): 0.5, ("Steel", "Water"): 0.5, ("Steel", "Electric"): 0.5, ("Steel", "Steel"): 0.5,
    
    # fairy type
    ("Fairy", "Fighting"): 2.0, ("Fairy", "Dragon"): 2.0, ("Fairy", "Dark"): 2.0,
    ("Fairy", "Fire"): 0.5, ("Fairy", "Poison"): 0.5, ("Fairy", "Steel"): 0.5,
}

def type_effectiveness(move_type, target_type):
    """
    This will serve to calculate the type effectiveness based on move and target types.
    
    Args:
        move_type (str): Type of the attacking move.
        target_type (str): Type of the target Pokémon.
    
    Returns:
        float: Effectiveness multiplier (e.g., 2.0, 0.5, 1.0).
    """
    return type_chart.get((move_type, target_type), 1.0)

# need to install this to get it to work
# !pip install langchain langchain-openai openai langchain-community tiktoken faiss-cpu --quiet

import os
import json
import openai
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file (optional)
# if you don't have your api key in a .env file. create a file 
# and store your api key in it

# make sure you are in same directory as the .py file
# create file named .env or in terminal touch .env
# code .env
# OPENAI_API=your_api_key_here
# to use it, do pip install python-dotenv --quiet


load_dotenv()

# Set OpenAI API key and change to your API key name
openai.api_key = os.getenv("PokemonAPI")
if not openai.api_key:
    raise ValueError("Missing OpenAI API key. Set OPENAI_API in your environment or .env file.")

# Define Pokémon data (Gen 2 specific)
# This dictionary contains the data of Pokémon with their stats, types, and available moves.
pokemon_data = {
    "Typhlosion": {
        "level": 100,  # Pokémon's level
        "type": ["Fire"],  # Pokémon's type(s)
        "moves": {  # Moves available for the Pokémon
            "Flamethrower": {"type": "Fire", "power": 95},  # Move details (type and base power)
            "Swift": {"type": "Normal", "power": 60},
            "Thunder Punch": {"type": "Electric", "power": 75},
            "Earthquake": {"type": "Ground", "power": 100},
        },
    },
    "Ampharos": {
        "level": 100,
        "type": ["Electric"],
        "moves": {
            "Thunderbolt": {"type": "Electric", "power": 95},
            "Fire Punch": {"type": "Fire", "power": 75},
            "Focus Blast": {"type": "Fighting", "power": 120},
            "reflect": {"type": "Psychic", "power": 0},  # Non-damaging move (power = 0)
        },
    },
}

# Gen 2 type chart
# Defines the effectiveness of Pokémon moves against specific types.
type_chart = {
    "Normal": {"strong_against": [], "weak_against": ["Rock", "Steel"], "immune_to": ["Ghost"]},
    "Fire": {"strong_against": ["Grass", "Bug", "Ice", "Steel"], "weak_against": ["Water", "Rock", "Fire", "Dragon"], "immune_to": []},
    "Water": {"strong_against": ["Fire", "Rock", "Ground"], "weak_against": ["Water", "Grass", "Dragon"], "immune_to": []},
    "Electric": {"strong_against": ["Water", "Flying"], "weak_against": ["Electric", "Grass", "Dragon"], "immune_to": ["Ground"]},
    "Grass": {"strong_against": ["Water", "Rock", "Ground"], "weak_against": ["Fire", "Grass", "Poison", "Flying", "Bug", "Dragon", "Steel"], "immune_to": []},
    "Ice": {"strong_against": ["Grass", "Ground", "Flying", "Dragon"], "weak_against": ["Fire", "Water", "Ice", "Steel"], "immune_to": []},
    "Fighting": {"strong_against": ["Normal", "Ice", "Rock", "Dark", "Steel"], "weak_against": ["Poison", "Flying", "Psychic", "Bug"], "immune_to": ["Ghost"]},
    "Poison": {"strong_against": ["Grass"], "weak_against": ["Poison", "Ground", "Rock", "Ghost"], "immune_to": ["Steel"]},
    "Ground": {"strong_against": ["Fire", "Electric", "Poison", "Rock", "Steel"], "weak_against": ["Grass", "Bug"], "immune_to": ["Flying"]},
    "Flying": {"strong_against": ["Grass", "Fighting", "Bug"], "weak_against": ["Electric", "Rock", "Steel"], "immune_to": []},
    "Psychic": {"strong_against": ["Fighting", "Poison"], "weak_against": ["Psychic", "Steel"], "immune_to": ["Dark"]},
    "Bug": {"strong_against": ["Grass", "Psychic", "Dark"], "weak_against": ["Fire", "Fighting", "Poison", "Flying", "Ghost", "Steel"], "immune_to": []},
    "Rock": {"strong_against": ["Fire", "Ice", "Flying", "Bug"], "weak_against": ["Fighting", "Ground", "Steel"], "immune_to": []},
    "Ghost": {"strong_against": ["Psychic", "Ghost"], "weak_against": ["Dark", "Steel"], "immune_to": ["Normal"]},
    "Dragon": {"strong_against": ["Dragon"], "weak_against": ["Steel"], "immune_to": []},
    "Dark": {"strong_against": ["Psychic", "Ghost"], "weak_against": ["Fighting", "Bug", "Dark"], "immune_to": []},
    "Steel": {"strong_against": ["Ice", "Rock"], "weak_against": ["Fire", "Water", "Electric", "Steel"], "immune_to": ["Poison"]},
}

# Pokémon data and type chart remain unchanged as defined in your code.

# Function to calculate move damage based on Gen 2 type chart, move power, and STAB.
def calculate_damage(attacker, defender, move):
    # Get the move details from the attacker's move set
    move_data = attacker["moves"].get(move)
    if not move_data:
        return 0

    move_type = move_data["type"]
    defender_types = defender["type"]

    # Determine type effectiveness multiplier
    effectiveness = 1
    for defender_type in defender_types:
        if defender_type in type_chart[move_type]["strong_against"]:
            effectiveness *= 2
        elif defender_type in type_chart[move_type]["weak_against"]:
            effectiveness *= 0.5
        elif defender_type in type_chart[move_type]["immune_to"]:
            effectiveness = 0

    # Check for Same Type Attack Bonus (STAB)
    stab = 1.5 if move_type in attacker["type"] else 1

    # Calculate total damage
    return move_data["power"] * effectiveness * stab


# Function to choose the best move for an attacker against a defender.
def choose_move(attacker_name, defender_name):
    attacker = pokemon_data[attacker_name]
    defender = pokemon_data[defender_name]

    move_damages = {}  # To store move damage calculations
    best_move = None
    max_damage = 0

    for move in attacker["moves"]:
        damage = calculate_damage(attacker, defender, move)
        move_damages[move] = damage
        if damage > max_damage:
            max_damage = damage
            best_move = move

    return {
        "action": "choose_move",
        "attacker": attacker_name,
        "defender": defender_name,
        "move_damages": move_damages,
        "chosen_move": best_move,
        "estimated_damage": max_damage,
    }


# Define mapping of functions for dynamic execution
FUNCTIONS = {
    "choose_move": choose_move,
}

# Define a function descriptor for OpenAI's function-calling feature
functions = [
    {
        "name": "choose_move",
        "description": "Choose the best move for the attacker Pokémon.",
        "parameters": {
            "type": "object",
            "properties": {
                "attacker_name": {"type": "string", "description": "The name of the attacking Pokémon."},
                "defender_name": {"type": "string", "description": "The name of the defending Pokémon."},
            },
            "required": ["attacker_name", "defender_name"],  # Required parameters for this function
        },
    }
]

# OpenAI API client change to your API key name
client = OpenAI(api_key=os.environ["PokemonAPI"])

# Initial messages and OpenAI call
messages = [
    {"role": "system", "content": "You are a Pokémon battle assistant, specialized in Gen 2 battles."},
    {"role": "user", "content": "My Typhlosion is battling Ampharos. List all of Typhlosion's moves with the calculated damage for each move. Then, recommend the most optimal move."},
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    functions=functions,
    function_call="auto",
)

# Convert the response to a dictionary
# response_dict = response.to_dict()

# Now you can print the response as a nicely formatted JSON
# print(json.dumps(response_dict, indent=2))
#print(response.choices[0].message)
def make_decision():
    if hasattr(response.choices[0].message, "function_call") and response.choices[0].message.function_call is not None:
        function_name = response.choices[0].message.function_call.name
        function_args = json.loads(response.choices[0].message.function_call.arguments)

        function_response = FUNCTIONS[function_name](**function_args)

        messages.append({"role": "assistant", "content": response.choices[0].message.content or "AI called a function without returning content."})
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response),
            }
        )
        #debugging
        for i, msg in enumerate(messages):
            if not isinstance(msg["content"], str):
                print(f"Invalid content in message[{i}]:", msg)

        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        print(final_response)
        return final_response.choices[0].message.content
    else:
        return response.choices[0].message.content or "AI response has no content."

print(make_decision())