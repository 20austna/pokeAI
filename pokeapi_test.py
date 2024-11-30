import requests

def get_move_flavor_text(move_name):
    """
    Fetches the flavor text for a given move from the PokeAPI.

    Parameters:
        move_name (str): The name of the Pokémon move.

    Returns:
        str: The flavor text for the move, or a message if not found.
    """
    url = f"https://pokeapi.co/api/v2/move/{move_name}/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        # Extract flavor text entries
        flavor_text_entries = data.get("flavor_text_entries", [])
        
        # Find the flavor text in English
        for entry in flavor_text_entries:
            if entry["language"]["name"] == "en":
                return entry["flavor_text"]
        
        return "Flavor text in English not found."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
import requests

def get_move_flavor_text(move_name):
    """
    Fetches the flavor text for a given move from the PokeAPI.

    Parameters:
        move_name (str): The name of the Pokémon move.

    Returns:
        str: The flavor text for the move, or a message if not found.
    """
    url = f"https://pokeapi.co/api/v2/move/{move_name}/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        # Extract flavor text entries
        flavor_text_entries = data.get("flavor_text_entries", [])
        
        # Find the flavor text in English
        for entry in flavor_text_entries:
            if entry["language"]["name"] == "en":
                return entry["flavor_text"]
        
        return "Flavor text in English not found."
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

# Test the function
if __name__ == "__main__":
    move_name = "stomp"  # Example move name
    flavor_text = get_move_flavor_text(move_name)
    print(f"Flavor text for move '{move_name}': {flavor_text}")

# Test the function
if __name__ == "__main__":
    move_name = "wrap"  # Example move name
    flavor_text = get_move_flavor_text(move_name)
    print(f"Flavor text for move '{move_name}': {flavor_text}")
