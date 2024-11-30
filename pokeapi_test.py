import requests

def get_move_flavor_text_by_generation(move_name, generation_name="gold-silver"):
    """
    Fetches the flavor text for a given move from the PokeAPI for a specific generation.

    Parameters:
        move_name (str): The name of the Pokémon move.
        generation_name (str): The version group of the Pokémon game (e.g., "gold-silver").

    Returns:
        str: The flavor text for the move in the specified generation, or a message if not found.
    """
    url = f"https://pokeapi.co/api/v2/move/{move_name}/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        # Extract flavor text entries
        flavor_text_entries = data.get("flavor_text_entries", [])
        
        # Find the flavor text in English for the specified generation
        for entry in flavor_text_entries:
            if (
                entry["language"]["name"] == "en" and 
                entry["version_group"]["name"] == generation_name
            ):
                return entry["flavor_text"]
        
        return f"Flavor text for generation '{generation_name}' not found in English."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Test the function
if __name__ == "__main__":
    move_name = "pound"  # Example move name
    generation_name = "gold-silver"  # Specify the generation (e.g., Generation II)
    flavor_text = get_move_flavor_text_by_generation(move_name, generation_name)
    print(f"Flavor text for move '{move_name}' in generation '{generation_name}': {flavor_text}")
