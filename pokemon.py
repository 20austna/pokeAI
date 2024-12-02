from moves import Move

import requests

def get_poke_data(poke_id):
    """
    Fetches detailed move data for a given move ID from the PokeAPI.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()

        # Extract relevant details
        poke_data = {
            "name": data.get("name", "Unknown").capitalize(),
            "types": [t["type"]["name"].capitalize() for t in data.get("types", [])],
            "base_stats": {stat["stat"]["name"]: stat["base_stat"] for stat in data.get("stats", [])},
            "abilities": [ability["ability"]["name"].capitalize() for ability in data.get("abilities", [])]
        }

        return poke_data
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

def create_moves(moves):
    i = 1
    moves_dict = {}
    for move in moves:
        key = f"move_{i}"
        value = Move(move.get("id"), move.get("current_move_pp"))
        moves_dict[key] = value
        i=i+1
    return moves_dict


class Pokemon:
    def __init__(self, id, moves, hp, attack, defense, special_attack, special_defense, speed, name="", current_mon=False, description="",types=None):
        """
        Initialize a new Pokemon object.

        :param id: ID of the Pokémon (int)
        :param types: List of types (e.g., ['Fire'], ['Water', 'Flying']) (list of str)
        :param hp: Hit Points (int)
        :param attack: Attack stat (int)
        :param defense: Defense stat (int)
        :param special_attack: Special Attack stat (int)
        :param special_defense: Special Defense stat (int)
        :param speed: Speed stat (int)
        :param description: A brief description of the Pokémon (str)
        """

        api_data = get_poke_data(id)

        if "error" in api_data:
            raise ValueError(f"Failed to fetch data for move with ID {id}: {api_data['error']}")

        self._data = {
            "id": id,
            "name": name or api_data["name"],
            "types": types or api_data["types"],
            "moves": create_moves(moves),
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "special_attack": special_attack,
            "special_defense": special_defense,
            "speed": speed,
            "description": description,
            "current_mon": current_mon
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
        String representation of the Pokemon object.
        """
        return f"{self._data}"

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

# print(Pokemon_1)
# my_moves = Pokemon_1._data.get("moves")
# print(my_moves.get('move_1').__getitem__('id'))
        

