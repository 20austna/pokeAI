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
from pokemon import Pokemon

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
# Pokémon data for the player and opponent

#example of 3 moves the pokemon will have
move_4 = {
    "id": 53,
    "move_pp_current": 15,
}

move_5 = {
    "id": 2,
    "move_pp_current": 35,  # Maximum PP for Pound
}

move_6 = {
    "id": 3,
    "move_pp_current": 25,  # Maximum PP for Karate Chop
}


#1: 'Pound', 2: 'Karate Chop'
Pokemon_1 = Pokemon(
    id=246,
    types=["Rock", "Ground"],
    moves = [move_4, move_5, move_6],
    hp=50,
    attack=64,
    defense=50,
    special_attack=45,
    special_defense=50,
    speed=41,
    description="Born deep underground, it comes aboveground and becomes a pupa once it has finished eating the surrounding soil."
)

your_pokemon = {
    "name": "Typhlosion",
    "level": 100,
    "type": ["Fire"],
    "moves": {
        "Flamethrower": {"type": "Fire", "power": 95, "pp": 5},
        "Swift": {"type": "Normal", "power": 60, "pp": 10},
        "Thunder Punch": {"type": "Electric", "power": 75, "pp": 0},  # Out of PP
        "Earthquake": {"type": "Ground", "power": 100, "pp": 3},
    },
}

opponent_pokemon = {
    "name": "Ampharos",
    "level": 100,
    "type": ["Electric"],
    "moves": {
        "Thunderbolt": {"type": "Electric", "power": 95, "pp": 8},
        "Fire Punch": {"type": "Fire", "power": 75, "pp": 5},
        "Focus Blast": {"type": "Fighting", "power": 120, "pp": 2},
        "Reflect": {"type": "Psychic", "power": 0, "pp": 10},  # Non-damaging move
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

# Function to calculate move damage based on Gen 2 type chart, move power, and STAB.
def calculate_damage(attacker, defender, move):
    move_data = attacker["moves"].get(move)
    if not move_data or move_data["pp"] <= 0:  # Check if move is out of PP
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

    move_damages = {}
    best_move = None
    max_damage = 0

    print("Moves type:", (your_pokemon["moves"])) 

    for move in your_pokemon["moves"]:
        # Skip moves with no PP
        if your_pokemon["moves"][move]["pp"] <= 0:
            continue
        damage = calculate_damage(your_pokemon, opponent_pokemon, move)
        move_damages[move] = damage
        if damage > max_damage:
            max_damage = damage
            best_move = move

    return {
        "action": "choose_move",
        "attacker": your_pokemon["name"],
        "defender": opponent_pokemon["name"],
        "move_damages": move_damages,
        "chosen_move": best_move,
        "estimated_damage": max_damage,
    }


# Define mapping of functions for dynamic execution
FUNCTIONS = {
    "choose_move": choose_move,
}

# OpenAI API client setup (unchanged)
client = OpenAI(api_key=os.environ["PokemonAPI"])

# Initial messages and OpenAI call
messages = [
    {"role": "system", "content": "You are a Pokémon battle assistant, specialized in Gen 2 battles."},
    {
        "role": "user",
        "content": f"My {your_pokemon['name']} is battling {opponent_pokemon['name']}. List all of {your_pokemon['name']}'s moves with the calculated damage for each move. Then, recommend the most optimal move."
    },
]

response = client.chat.completions.create(
    model="gpt-4o",  # Use appropriate model here
    messages=messages,
    functions=[{
        "name": "choose_move",
        "description": "Choose the best move for the attacker Pokémon.",
        "parameters": {
            "type": "object",
            "properties": {
                "attacker_name": {"type": "string", "description": "The name of the attacking Pokémon."},
                "defender_name": {"type": "string", "description": "The name of the defending Pokémon."},
            },
            "required": ["attacker_name", "defender_name"],
        },
    }],
    function_call="auto",
)

def make_decision():
    # If the response includes a function call, process it
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
        #print(final_response)
        return final_response.choices[0].message.content
    else:
        return response.choices[0].message.content or "AI response has no content."

#print(make_decision())
