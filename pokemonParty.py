from pokemon import Pokemon

class PokemonParty:
    def __init__(self, max_party_size=6, party=None):
        """
        Initialize a PokemonParty object.

        :param max_party_size: Maximum number of Pokemon allowed
            in the part (default)
        """
        self.max_part_size = max_party_size
        self.party = party

    def add_pokemon(self, pokemon):
        """
        Add a Pokemon to the party

        :param pokemon: A Pokemon object to add
        :raises ValueError: If the party is full
        """
        if len(self.party) >= self.max_party_size:
            raise ValueError("Party is full. Cannot add more Pokémon.")
        if not isinstance(pokemon, Pokemon):
            raise ValueError("Only Pokemon objects can be added to the party.")
        self.party.append(pokemon)

    # if needed if we decide for the AI to be able to 
    # catch pokemon
    def remove_pokemon(self, index):
        self.party.pop(index)

    def list_pokemon(self):
        """
        List all Pokemon in the party.
        
        :return A list of Pokemon names
        """
        return [pokemon['name'] for pokemon in self.party]
    
    def __len__(self):
        """
        Return the number of the Pokemon in the party
        """
    
    def __getitem__(self, index):
        """
        Get a Pokémon by index.
        """
        return self.party[index]

    def __str__(self):
        """
        String representation of the PokemonParty object.
        """
        return f"PokemonParty with {len(self.party)} Pokémon: {[pokemon['name'] for pokemon in self.party]}"