import requests

def get_move_data(move_id):
    """
    Fetches detailed move data for a given move ID from the PokeAPI.
    """
    url = f"https://pokeapi.co/api/v2/move/{move_id}/"
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
            "max_move_pp": data.get("pp", "N/A"),
            "attack_type": data["damage_class"]["name"] if data.get("damage_class") else "Unknown",
            "description": next(
                (entry["effect"] for entry in data.get("effect_entries", [])
                 if entry["language"]["name"] == "en"), None
            ),
        }

        return move_data
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

class Move:
    def __init__(self, id, current_move_pp, name = None, move_type=None, power=None, accuracy=None, max_move_pp=None, attack_type=None, description=None):
        """
        Initialize a new Move object.

        :param id: id
        :param move_type: Type of the move (e.g., Fire, Water) (str)
        :param power: Power of the move (int)
        :param accuracy: Accuracy percentage of the move (int)
        :param move_pp: Maximum Power Points (PP) for the move (int)
        :param attack_type: Attack type (Physical or Special) (str)
        :param description: A brief description of the move (str)
        """
        api_data = get_move_data(id)

        if "error" in api_data:
            raise ValueError(f"Failed to fetch data for move with ID {id}: {api_data['error']}")

        # Fill parameters with API data if not provided
        self._data = {
            "id": id,
            "name": name or api_data["name"],
            "move_type": move_type or api_data["move_type"],
            "power": power or api_data["power"],
            "accuracy": accuracy or api_data["accuracy"],
            "max_move_pp": max_move_pp or api_data["max_move_pp"],
            "current_move_pp": current_move_pp,
            "attack_type": attack_type or api_data["attack_type"],
            "description": description or api_data["description"],
        }

    def __getitem__(self, key):
        """
        Get an item by key.
        """
        return self._data[key]

    def __setitem__(self, key, value):
        """
        Set an item by key.
        """
        self._data[key] = value

    def __delitem__(self, key):
        """
        Delete an item by key.
        """
        del self._data[key]

    def __iter__(self):
        """
        Return an iterator over the keys.
        """
        return iter(self._data)

    def __len__(self):
        """
        Return the number of items.
        """
        return len(self._data)

    def __str__(self):
        """
        String representation of the Move object.
        """
        return f"{self._data}"
    
    def __repr__(self):
        return self.__str__()

    def keys(self):
        """
        Return the keys of the dictionary.
        """
        return self._data.keys()

    def values(self):
        """
        Return the values of the dictionary.
        """
        return self._data.values()

    def items(self):
        """
        Return the items of the dictionary.
        """
        return self._data.items()

