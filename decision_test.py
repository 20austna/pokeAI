import os
import json
import openai
from dotenv import load_dotenv

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


import os
import json
from openai import OpenAI

# Define Pokémon data (Gen 2 specific)
# This dictionary contains the data of Pokémon with their stats, types, and available moves.
# Pokémon data for the player and opponent
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
def choose_move(attacker, defender):
    # print(attacker)
    # print(attacker['moves'])


    move_damages = {}
    best_move = None
    max_damage = 0

    # print("Moves type:", (your_pokemon["moves"])) 

    for move in attacker["moves"]:
        # Skip moves with no PP
        if attacker["moves"][move]["pp"] <= 0:
            continue
        damage = calculate_damage(attacker, defender, move)
        move_damages[move] = damage
        if damage > max_damage:
            max_damage = damage
            best_move = move

    return {
        "action": "choose_move",
        "attacker": attacker["name"],
        "defender": defender["name"],
        "move_damages": move_damages,
        "chosen_move": best_move,
        "estimated_damage": max_damage,
    }

def serialize_pokemon_data(pokemon):
    try:
        return json.dumps(pokemon, indent=2, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        print(f"Error serializing Pokémon data: {e}")
        return "{}"  # Return an empty JSON object if serialization fails
    
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
        "content": (
            f"My {your_pokemon['name']} is battling {opponent_pokemon['name']}."
            f"Here is the detailed information for both Pokémon:"
            f"Attacker:\n{serialize_pokemon_data(your_pokemon)}"
            f"Defender:\n{serialize_pokemon_data(opponent_pokemon)}"
            f"List all of {your_pokemon['name']}'s moves with the calculated damage for each move. "
            f"Then, recommend the most optimal move."
        ),
    },
]

# Define the function schema
function_schema = {
    "name": "choose_move",
    "description": "Choose the best move for the attacker Pokémon.",
    "parameters": {
        "type": "object",
        "properties": {
            "attacker": {
                "type": "object",
                "description": "The attacking Pokémon with all its details.",
                "properties": {
                    "name": {"type": "string", "description": "The name of the attacking Pokémon."},
                    "level": {"type": "integer", "description": "The level of the attacking Pokémon."},
                    "type": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The types of the attacking Pokémon.",
                    },
                    "moves": {
                        "type": "object",
                        "description": "The moves the Pokémon can use.",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "description": "The type of the move."},
                                "power": {"type": "integer", "description": "The power of the move."},
                                "pp": {"type": "integer", "description": "The remaining PP of the move."},
                            },
                            "required": ["type", "power", "pp"],
                        },
                    },
                },
                "required": ["name", "level", "type", "moves"],
            },
            "defender": {
                "type": "object",
                "description": "The defending Pokémon with all its details.",
                "properties": {
                    "name": {"type": "string", "description": "The name of the defending Pokémon."},
                    "level": {"type": "integer", "description": "The level of the defending Pokémon."},
                    "type": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "The types of the defending Pokémon.",
                    },
                    "moves": {
                        "type": "object",
                        "description": "The moves the Pokémon can use.",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "description": "The type of the move."},
                                "power": {"type": "integer", "description": "The power of the move."},
                                "pp": {"type": "integer", "description": "The remaining PP of the move."},
                            },
                            "required": ["type", "power", "pp"],
                        },
                    },
                },
                "required": ["name", "level", "type", "moves"],
            },
        },
        "required": ["attacker", "defender"],
    },
}

# OpenAI API call
response = client.chat.completions.create(
    model="gpt-4-0613",
    messages=messages,
    functions=[function_schema],
    function_call="auto",
)

# print(response)

'''
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
'''
print(response)
#print("Response from OpenAI:", response.choices[0].message)
# If the response includes a function call, process it
"""
in a function have it pull in the entire dataset/dictionary of to pull to other methods
so like have the arguments be all of your_pokemon and all of opponent_pokemon
"""
if hasattr(response.choices[0].message, "function_call"):
    function_name = response.choices[0].message.function_call.name
    function_args = json.loads(response.choices[0].message.function_call.arguments)

    #print(function_args)
    function_response = FUNCTIONS[function_name](**function_args)

    # Update messages with function response
    messages.append({"role": "assistant", "content": response.choices[0].message.content or "AI called a function without returning content."})
    messages.append({
        "role": "function",
        "name": function_name,
        "content": json.dumps(function_response),
    })

    final_response = client.chat.completions.create(
        model="gpt-4",  # Choose appropriate model
        messages=messages,
    )
    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content or "AI response has no content.")