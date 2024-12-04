import openai
import os
from pokemon import Pokemon
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Set OpenAI API key and change to your API key name
#openai.api_key = os.getenv("PokemonAPI")

"""
 The type chart defines the relationships between Pokémon types for damage calculation.
 It specifies which types are strong against, weak against, or immune to others.
 The structure is a dictionary where the keys are the move types, and the values
 are dictionaries detailing the interactions with other types:
   - "strong_against": A list of types that take 2x damage from this move type.
   - "weak_against": A list of types that take 0.5x damage from this move type.
   - "immune_to": A list of types that take 0 damage from this move type.
"""
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

# Function to calculate the damage dealt by a move in a Pokémon battle.
# Uses Generation 2 type chart mechanics, move power, and STAB (Same Type Attack Bonus).
def calculate_damage(attacker, defender, move):
    # Check if move is out of PP   
    if move["current_move_pp"] <= 0:
        return 0

    move_type = move["move_type"]

    # Initialize a list to store multipliers affecting damage calculation.
    # Default value is 1 (no effect on damage).
    damage_multiplier = [1]
    
    # Determine type effectiveness multiplier by checking defender's types.
    for defender_type in defender:
        defender_type = defender_type.lower()
        # If the move's type is strong against the defender's type, double the damage.
        if defender_type in type_chart[move_type]["strong_against"]:
            damage_multiplier.append(2)
        # If the move's type is weak against the defender's type, halve the damage.
        elif defender_type in type_chart[move_type]["weak_against"]:
            damage_multiplier.append(0.5)
         # If the move's type has no effect on the defender's type, set damage to 0.
        elif defender_type in type_chart[move_type]["immune_to"]:
            damage_multiplier.append(0)
            

    # Check for Same Type Attack Bonus (STAB)
    for attack_type in attacker:
        attack_type = attack_type.lower()
        # If the attacker has the same type as the move, apply the STAB multiplier.
        if attack_type in move_type:
            damage_multiplier.append(1.5)
            break
    
    # Calculate the final damage multiplier by multiplying all factors.
    result = 1
    for num in damage_multiplier:
        result *= num

    # Return the final damage, which is the move's power multiplied by the overall multiplier.
    return move['power'] * result


# Function to generate a prompt for an OpenAI model to determine the best move in a Pokémon battle.
def generate_prompt(attacker, defender):
    # Get the moves for the attacker
    pokemon_moves = attacker._data.get("moves", {})

    # Initialize the prompt with instructions and details about the attacker.
    prompt = f"""
    You are a Pokémon battle assistant. Given the information below, choose the best move for {attacker['name']} to use against {defender['name']}.
    Consider the type effectiveness, move power, current PP, total move power, and accuracy to determine the best move.

    Attacker: {attacker['name']}
    Type(s): {attacker['types']}
    Moves:
    """

    move_damages = {}

    # Iterate through the attacker's moves and calculate their potential effectiveness.
    for move_key, move_data in pokemon_moves.items():   
        # Calculate the total power of the move based on type effectiveness and other factors.
        total_power = calculate_damage(attacker._data.get("types"), defender._data.get("types"), move_data) 
        move_damages[move_data['name']] = total_power
        prompt += f"  - {move_data['name']} (Type: {move_data['move_type']}, Power: {move_data['power']}, Accuracy: {move_data['accuracy']}, Current PP: {move_data['current_move_pp']}, Total Power: {total_power})\n"
    
    prompt += f"\nDefender: {defender['name']}\nType: {', '.join(defender['types'])}\n\n"

    prompt += """
    Based on the provided information, determine which move will be the most effective considering type advantages, move power, accuracy, and current PP left.
    Return only the name of the most optimal move."""

    # Return fully constructed prompt
    return prompt

# Function to make a decision using OpenAI's API to select the optimal move in a Pokémon battle.
def make_decision(attacker, defender):
    # Create a structured message for the OpenAI API, including instructions and context.
    messages = [
        {
            "role": "system", 
            "content": "You are a Pokémon battle assistant. Your task is to choose the best move for the attacker against the defender. Consider the attacker's moves, type effectiveness, move power, and accuracy, but only provide the most optimal move as the output. Keep the response short and clear."
        },
        {
            "role": "user", 
            "content": generate_prompt(attacker, defender)
        },
    ]

    # Initialize the OpenAI client using the API key stored in an environment variable.
    client = OpenAI(api_key=os.environ["PokemonAPI"])

    # Make an API call to OpenAI's chat model to generate a response based on the messages.
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=50,
        temperature=0.5,
    )

    # Extract the AI's decision from the response.
    decision = response.choices[0].message.content
    return decision
