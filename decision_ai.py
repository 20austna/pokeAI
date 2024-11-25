def make_decision(our_pokemon, opponent_pokemon, menu_state):
    """
    This will serve as an AI decision-making function in order to decide what the best move 
    would be during in a Pokemon battle.
    
    Args:
        our_pokemon: our own pokemon object.
        opponent_pokemon: opponent's pokemon object.
        menu_state (str): current menu state (ex: "Fight").
    
    Returns:
        str: the best move to use.
    """
    
    # we want to make sure we are in fight mode. if we aren't, then
    # no decision will be made
    if menu_state != "Fight":
        print("Not in the Fight menu so no decision made.")
        return None
    
    # simple debug statements
    print(f"Opponent HP: {opponent_pokemon.current_HP}/{opponent_pokemon.max_HP}")
    print(f"Opponent Level: {opponent_pokemon.level}")
    
    # filter out any moves that have 0 pp
    available_moves = [move for move in our_pokemon.moves if move["move_pp"] > 0]
    # if ALL our moves have no pp left than use struggle
    if not available_moves:
        print("No available moves left! Struggle must be used.")
        return "Struggle"
    
    # determine what the best move is based on effectiveness and power
    best_move = None
    # this variable will serve to track what the most effective move is
    best_score = -1 
    
    for move in available_moves:
        # get move stats
        move_name = move["name"]
        move_type = move["move_type"]
        move_power = move["power"]
        move_pp = move["move_pp"]
        
        # calculate the type effectiveness 
        # (if we do not know what the type is then use a default value of 1.0)
        effectiveness = type_effectiveness(move_type, opponent_pokemon.type1)
        if opponent_pokemon.type2:
            effectiveness = max(effectiveness, type_effectiveness(move_type, opponent_pokemon.type2))
        
        # calculate a score based on power and effectiveness which is the damage multiplier
        score = move_power * effectiveness
        if score > best_score:
            best_score = score
            best_move = move_name
    
    print(f"AI selected move: {best_move}")
    return best_move


type_chart = {
    # fire type
    ("Fire", "Grass"): 2.0, ("Fire", "Bug"): 2.0, ("Fire", "Ice"): 2.0, ("Fire", "Steel"): 2.0,
    ("Fire", "Water"): 0.5, ("Fire", "Fire"): 0.5, ("Fire", "Rock"): 0.5, ("Fire", "Dragon"): 0.5,
    
    # water type
    ("Water", "Fire"): 2.0, ("Water", "Ground"): 2.0, ("Water", "Rock"): 2.0,
    ("Water", "Water"): 0.5, ("Water", "Grass"): 0.5, ("Water", "Dragon"): 0.5,
    
    # grass type
    ("Grass", "Water"): 2.0, ("Grass", "Ground"): 2.0, ("Grass", "Rock"): 2.0,
    ("Grass", "Fire"): 0.5, ("Grass", "Grass"): 0.5, ("Grass", "Poison"): 0.5,
    ("Grass", "Flying"): 0.5, ("Grass", "Bug"): 0.5, ("Grass", "Dragon"): 0.5, ("Grass", "Steel"): 0.5,
    
    # electric type
    ("Electric", "Water"): 2.0, ("Electric", "Flying"): 2.0,
    ("Electric", "Electric"): 0.5, ("Electric", "Grass"): 0.5, ("Electric", "Dragon"): 0.5,
    ("Electric", "Ground"): 0.0,
    
    # ice type
    ("Ice", "Grass"): 2.0, ("Ice", "Ground"): 2.0, ("Ice", "Flying"): 2.0, ("Ice", "Dragon"): 2.0,
    ("Ice", "Fire"): 0.5, ("Ice", "Water"): 0.5, ("Ice", "Ice"): 0.5, ("Ice", "Steel"): 0.5,
    
    # fighting type
    ("Fighting", "Normal"): 2.0, ("Fighting", "Ice"): 2.0, ("Fighting", "Rock"): 2.0, ("Fighting", "Dark"): 2.0,
    ("Fighting", "Steel"): 2.0,
    ("Fighting", "Poison"): 0.5, ("Fighting", "Flying"): 0.5, ("Fighting", "Psychic"): 0.5, ("Fighting", "Bug"): 0.5,
    ("Fighting", "Fairy"): 0.5, ("Fighting", "Ghost"): 0.0,
    
    # poison type
    ("Poison", "Grass"): 2.0, ("Poison", "Fairy"): 2.0,
    ("Poison", "Poison"): 0.5, ("Poison", "Ground"): 0.5, ("Poison", "Rock"): 0.5, ("Poison", "Ghost"): 0.5,
    ("Poison", "Steel"): 0.0,
    
    # ground type
    ("Ground", "Fire"): 2.0, ("Ground", "Electric"): 2.0, ("Ground", "Poison"): 2.0, ("Ground", "Rock"): 2.0,
    ("Ground", "Steel"): 2.0,
    ("Ground", "Grass"): 0.5, ("Ground", "Bug"): 0.5, ("Ground", "Flying"): 0.0,
    
    # flying type
    ("Flying", "Grass"): 2.0, ("Flying", "Fighting"): 2.0, ("Flying", "Bug"): 2.0,
    ("Flying", "Electric"): 0.5, ("Flying", "Rock"): 0.5, ("Flying", "Steel"): 0.5,
    
    # psychic type
    ("Psychic", "Fighting"): 2.0, ("Psychic", "Poison"): 2.0,
    ("Psychic", "Psychic"): 0.5, ("Psychic", "Steel"): 0.5, ("Psychic", "Dark"): 0.0,
    
    # bug type
    ("Bug", "Grass"): 2.0, ("Bug", "Psychic"): 2.0, ("Bug", "Dark"): 2.0,
    ("Bug", "Fire"): 0.5, ("Bug", "Fighting"): 0.5, ("Bug", "Poison"): 0.5, ("Bug", "Flying"): 0.5,
    ("Bug", "Ghost"): 0.5, ("Bug", "Steel"): 0.5, ("Bug", "Fairy"): 0.5,
    
    # rock type
    ("Rock", "Fire"): 2.0, ("Rock", "Ice"): 2.0, ("Rock", "Flying"): 2.0, ("Rock", "Bug"): 2.0,
    ("Rock", "Fighting"): 0.5, ("Rock", "Ground"): 0.5, ("Rock", "Steel"): 0.5,
    
    # ghost type
    ("Ghost", "Psychic"): 2.0, ("Ghost", "Ghost"): 2.0,
    ("Ghost", "Dark"): 0.5, ("Ghost", "Normal"): 0.0,
    ("Ghost", "Fairy"): 0.5,
    
    # dragon type
    ("Dragon", "Dragon"): 2.0,
    ("Dragon", "Steel"): 0.5, ("Dragon", "Fairy"): 0.0,
    
    # dark type
    ("Dark", "Psychic"): 2.0, ("Dark", "Ghost"): 2.0,
    ("Dark", "Fighting"): 0.5, ("Dark", "Dark"): 0.5, ("Dark", "Fairy"): 0.5,
    
    # steel type
    ("Steel", "Ice"): 2.0, ("Steel", "Rock"): 2.0, ("Steel", "Fairy"): 2.0,
    ("Steel", "Fire"): 0.5, ("Steel", "Water"): 0.5, ("Steel", "Electric"): 0.5, ("Steel", "Steel"): 0.5,
    
    # fairy type
    ("Fairy", "Fighting"): 2.0, ("Fairy", "Dragon"): 2.0, ("Fairy", "Dark"): 2.0,
    ("Fairy", "Fire"): 0.5, ("Fairy", "Poison"): 0.5, ("Fairy", "Steel"): 0.5,
}

def type_effectiveness(move_type, target_type):
    """
    This will serve to calculate the type effectiveness based on move and target types.
    
    Args:
        move_type (str): Type of the attacking move.
        target_type (str): Type of the target Pokémon.
    
    Returns:
        float: Effectiveness multiplier (e.g., 2.0, 0.5, 1.0).
    """
    return type_chart.get((move_type, target_type), 1.0)
