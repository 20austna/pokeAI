import requests

def get_move_data(move_name, generation_name="gold-silver"):
    """
    Fetches detailed move data for a given move from the PokeAPI, including specific attributes.

    Parameters:
        move_name (str): The name of the Pokémon move.
        generation_name (str): The version group of the Pokémon game (e.g., "gold-silver").

    Returns:
        dict: A dictionary containing move details.
    """
    url = f"https://pokeapi.co/api/v2/move/{move_name}/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Extract relevant details
        move_data = {
            "id": data.get("id"),
            "name": data.get("name"),
            "move_type": data["type"]["name"] if data.get("type") else "Unknown",
            "power": data.get("power", "N/A"),
            "accuracy": data.get("accuracy", "N/A"),
            "move_pp": data.get("pp", "N/A"),
            "attack_type": data["damage_class"]["name"] if data.get("damage_class") else "Unknown",
            "description": None,
            "flavor_text": None,
        }

        # Extract English description
        for entry in data.get("effect_entries", []):
            if entry["language"]["name"] == "en":
                move_data["description"] = entry["effect"]
                break

        # Extract English flavor text for the specified generation
        for entry in data.get("flavor_text_entries", []):
            if (
                entry["language"]["name"] == "en" and 
                entry["version_group"]["name"] == generation_name
            ):
                move_data["flavor_text"] = entry["flavor_text"]
                break

        return move_data
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

# Test the function
if __name__ == "__main__":
    move_name = "pound"  # Example move name
    generation_name = "gold-silver"  # Specify the generation (e.g., Generation II)
    move_details = get_move_data(move_name, generation_name)
    
    if "error" in move_details:
        print(move_details["error"])
    else:
        print("Move Details:")
        print(f"ID: {move_details['id']}")
        print(f"Name: {move_details['name']}")
        print(f"Move Type: {move_details['move_type']}")
        print(f"Power: {move_details['power']}")
        print(f"Accuracy: {move_details['accuracy']}")
        print(f"PP: {move_details['move_pp']}")
        print(f"Attack Type: {move_details['attack_type']}")
        print(f"Description: {move_details['description']}")
        print(f"Flavor Text (Generation {generation_name}): {move_details['flavor_text']}")
    