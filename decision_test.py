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
    "current_move_pp": 15,
}

move_5 = {
    "id": 91,
    "current_move_pp": 10,  # Maximum PP for Pound
}

move_6 = {
    "id": 3,
    "current_move_pp": 25,  # Maximum PP for double slap
}

#1: 'Pound', 2: 'Karate Chop'
Pokemon_1 = Pokemon(
    id=246,
    #types=["Rock", "Ground"],
    moves = [move_4, move_5, move_6],
    hp=50,
    attack=64,
    defense=50,
    special_attack=45,
    special_defense=50,
    speed=41,
    description="Born deep underground, it comes aboveground and becomes a pupa once it has finished eating the surrounding soil."
)

Pokemon_2 = Pokemon(
    id=6,
    #types=["Fire"],
    moves = [move_4],
    hp=50,
    attack=64,
    defense=50,
    special_attack=45,
    special_defense=50,
    speed=41,
    description="Born deep underground, it comes aboveground and becomes a pupa once it has finished eating the surrounding soil."
)

#print(Pokemon_2)
#print(Pokemon_1)
#print(Pokemon_1["moves"])

# Gen 2 type chart
# Defines the effectiveness of Pokémon moves against specific types.
type_chart = {
    "normal": {"strong_against": [], "weak_against": ["rock", "steel"], "immune_to": ["ghost"]},
    "fire": {"strong_against": ["grass", "bug", "ice", "steel"], "weak_against": ["water", "rock", "fire", "dragon"], "immune_to": []},
    "water": {"strong_against": ["fire", "rock", "ground"], "weak_against": ["water", "grass", "dragon"], "immune_to": []},
    "electric": {"strong_against": ["water", "flying"], "weak_against": ["electric", "grass", "dragon"], "immune_to": ["ground"]},
    "grass": {"strong_against": ["water", "rock", "ground"], "weak_against": ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"], "immune_to": []},
    "ice": {"strong_against": ["grass", "ground", "flying", "dragon"], "weak_against": ["fire", "water", "ice", "steel"], "immune_to": []},
    "fighting": {"strong_against": ["normal", "ice", "rock", "dark", "steel"], "weak_against": ["poison", "flying", "psychic", "bug"], "immune_to": ["ghost"]},
    "poison": {"strong_against": ["grass"], "weak_against": ["poison", "ground", "rock", "ghost"], "immune_to": ["steel"]},
    "ground": {"strong_against": ["fire", "electric", "poison", "rock", "steel"], "weak_against": ["grass", "bug"], "immune_to": ["flying"]},
    "flying": {"strong_against": ["grass", "fighting", "bug"], "weak_against": ["electric", "rock", "steel"], "immune_to": []},
    "psychic": {"strong_against": ["fighting", "poison"], "weak_against": ["psychic", "steel"], "immune_to": ["dark"]},
    "bug": {"strong_against": ["grass", "psychic", "dark"], "weak_against": ["fire", "fighting", "poison", "flying", "ghost", "steel"], "immune_to": []},
    "rock": {"strong_against": ["fire", "ice", "flying", "bug"], "weak_against": ["fighting", "ground", "steel"], "immune_to": []},
    "ghost": {"strong_against": ["psychic", "ghost"], "weak_against": ["dark", "steel"], "immune_to": ["normal"]},
    "dragon": {"strong_against": ["dragon"], "weak_against": ["steel"], "immune_to": []},
    "dark": {"strong_against": ["psychic", "ghost"], "weak_against": ["fighting", "bug", "dark"], "immune_to": []},
    "steel": {"strong_against": ["ice", "rock"], "weak_against": ["fire", "water", "electric", "steel"], "immune_to": ["poison"]},
}


# Function to calculate move damage based on Gen 2 type chart, move power, and STAB.
def calculate_damage(attacker, defender, move):
    #print("attacker: ", attacker)
    #print("defender: ", defender)
    #print("move: ", move)
    
    if move["current_move_pp"] <= 0:  # Check if move is out of PP
        return 0

    move_type = move["move_type"]
    #print(move_type)

    damage_multiplier = [1]
    # Determine type effectiveness multiplier
    for defender_type in defender:
        defender_type = defender_type.lower()
        #print("defender_types:", defender_type)
        if defender_type in type_chart[move_type]["strong_against"]:
            damage_multiplier.append(2)
        elif defender_type in type_chart[move_type]["weak_against"]:
            damage_multiplier.append(0.5)
        elif defender_type in type_chart[move_type]["immune_to"]:
            damage_multiplier.append(0)

    # Check for Same Type Attack Bonus (STAB)
    for attack_type in attacker:
        attack_type = attack_type.lower()
        #print("attack_type: ", attack_type)
        if attack_type in move_type:
            damage_multiplier.append(1.5)
            break
    
    result = 1
    for num in damage_multiplier:
        result *= num

    #print(damage_multiplier)
    #print(result)
    return move["power"] * result

# Function to choose the best move for an attacker against a defender.
def choose_move(attacker_name, defender_name):
    pokemon_moves = attacker_name._data.get("moves", {})
    move_damages = {}
    best_move = None
    max_damage = 0

    # print(pokemon_moves)
    #print(move_count)
    #print("Moves type:", (your_pokemon["moves"])) 

    for move_key, move_data in pokemon_moves.items():
        #print(move_key)
        damage = calculate_damage(attacker_name._data.get("types"), defender_name._data.get("types"), move_data)
        #print(damage)
        move_damages[move_data['name']] = damage
    
    return {
        "action": "choose_move",
        "attacker": attacker_name["name"],
        "defender": defender_name["name"],
        "move_damages": move_damages,
        #"chosen_move": best_move,
        "estimated_damage": max_damage,
    }

def make_decision(Pokemon_1, Pokemon_2):
    # OpenAI API client setup (unchanged)
    client = OpenAI(api_key=os.environ["PokemonAPI"])

    # Initial messages and OpenAI call
    messages = [
        {"role": "system", "content": "You are a Pokémon battle assistant, specialized in Gen 2 battles."},
        {
            "role": "user",
            "content": f"My {Pokemon_1['name']} is battling {Pokemon_2['name']}. List all of {Pokemon_1['name']}'s moves with the calculated damage for each move. Then, recommend the most optimal move."
        },
    ]

    #print("message: ", messages)

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

    # If the response includes a function call, process it
    if hasattr(response.choices[0].message, "function_call") and response.choices[0].message.function_call is not None:
        # Assuming the response from OpenAI includes a function call
        function_name = response.choices[0].message.function_call.name
        function_response = choose_move(Pokemon_1, Pokemon_2)

        # Update messages with function response
        messages.append({"role": "assistant", "content": response.choices[0].message.content or "AI called a function without returning content."})
        messages.append({
            "role": "function",
            "name": function_name,
            "content": json.dumps(function_response),
        })

        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        #print(final_response)
        return final_response.choices[0].message.content
    else:
        return response.choices[0].message.content or "AI response has no content."

#print(make_decision(Pokemon_1, Pokemon_2))
print(make_decision(Pokemon_1, Pokemon_2))

