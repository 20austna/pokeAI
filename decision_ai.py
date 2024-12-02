import openai
import os
from pokemon import Pokemon
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Set OpenAI API key and change to your API key name
openai.api_key = os.getenv("PokemonAPI")

# Example Pokémon objects
move_4 = {
    "id": 53,
    "current_move_pp": 2,
}

move_5 = {
    "id": 91,
    "current_move_pp": 10,  # Maximum PP for Pound
}

move_6 = {
    "id": 3,
    "current_move_pp": 25,  # Maximum PP for double slap
}

move_7 = {
    "id": 157,
    "current_move_pp": 10,  # Maximum PP for double slap
}

#1: 'Pound', 2: 'Karate Chop'
Pokemon_1 = Pokemon(
    id=246,
    #types=["Rock", "Ground"],
    moves = [move_4, move_5, move_6, move_7],
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
    return move['power'] * result


# Function to generate the prompt for OpenAI
def generate_prompt(attacker, defender):
    # Get the moves for the attacker
    pokemon_moves = attacker._data.get("moves", {})

    prompt = f"""
    You are a Pokémon battle assistant. Given the information below, choose the best move for {attacker['name']} to use against {defender['name']}.
    Consider the type effectiveness, move power, current PP, total move power, and accuracy to determine the best move.

    Attacker: {attacker['name']}
    Type(s): {attacker['types']}
    Moves:
    """

    move_damages = {}
    # Add the attacker's moves to the prompt
    for move_key, move_data in pokemon_moves.items():   
        # Check type effectiveness for each move against the defender
        
        damage = calculate_damage(attacker._data.get("types"), defender._data.get("types"), move_data)
        #print(damage)
        
        move_damages[move_data['name']] = damage

        #if damage != 0: 
        prompt += f"  - {move_data['name']} (Type: {move_data['move_type']}, Power: {move_data['power']}, Accuracy: {move_data['accuracy']}, Current PP: {move_data['current_move_pp']}, Total Power: {damage})\n"
        #elif damage == 0:
            #continue
    
    # Add defender's name and typing to the prompt
    prompt += f"\nDefender: {defender['name']}\nType: {', '.join(defender['types'])}\n\n"

    prompt += """
    Based on the provided information, determine which move will be the most effective considering type advantages, move power, accuracy, and current PP left.
    Return only the name of the most optimal move."""

    return prompt

#print(generate_prompt(Pokemon_1, Pokemon_2))

# Function to make a decision using OpenAI
def make_decision(attacker, defender):
    # Create the messages structure for the API
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

    # OpenAI API client setup (unchanged)
    client = OpenAI(api_key=os.environ["PokemonAPI"])

    # Make the API call to OpenAI
    response = client.chat.completions.create(
        model="gpt-4",  # You can use a different engine like "gpt-4" or "gpt-3.5-turbo"
        messages=messages,
        max_tokens=50,
        temperature=0.5,
    )

    # Parse the AI's decision
    decision = response.choices[0].message.content
    return decision

# Call the function to make a decision
#best_move_decision = make_decision(Pokemon_1, Pokemon_2)

# Print the result
#print(f"Select {make_decision(Pokemon_1, Pokemon_2)}")