move_dict =  {0: '[glitchy]', 1: 'Pound', 2: 'Karate Chop', 3: 'Doubleslap', 4: 'Comet Punch', 
              5: 'Mega Punch', 6: 'Pay Day', 7: 'Fire Punch', 8: 'Ice Punch', 9: 'Thunderpunch', 
              10: 'Scratch', 11: 'Vicegrip', 12: 'Guillotine', 13: 'Razor Wind', 14: 'Swords Dance', 
              15: 'Cut', 16: 'Gust', 17: 'Wing Attack', 18: 'Whirlwind', 19: 'Fly', 
              20: 'Bind', 21: 'Slam', 22: 'Vine Whip', 23: 'Stomp', 24: 'Double Kick', 
              25: 'Mega Kick', 26: 'Jump Kick', 27: 'Rolling Kick', 28: 'Sand Attack', 29: 'Headbutt', 
              30: 'Horn Attack', 31: 'Fury Attack', 32: 'Horn Drill', 33: 'Tackle', 34: 'Body Slam', 
              35: 'Wrap', 36: 'Take Down', 37: 'Thrash', 38: 'Double-Edge', 39: 'Tail Whip', 
              40: 'Poison Sting', 41: 'Twineedle', 42: 'Pin Missile', 43: 'Leer', 44: 'Bite', 
              45: 'Growl', 46: 'Roar', 47: 'Sing', 48: 'Supersonic', 49: 'Sonicboom', 
              50: 'Disable', 51: 'Acid', 52: 'Ember', 53: 'Flamethrower', 54: 'Mist', 
              55: 'Water Gun', 56: 'Hydro Pump', 57: 'Surf', 58: 'Ice Beam', 59: 'Blizzard', 
              60: 'Psybeam', 61: 'Bubblebeam', 62: 'Aurora Beam', 63: 'Hyper Beam', 64: 'Peck', 
              65: 'Drill Peck', 66: 'Submission', 67: 'Low Kick', 68: 'Counter', 69: 'Seismic Toss', 
              70: 'Strength', 71: 'Absorb', 72: 'Mega Drain', 73: 'Leech Seed', 74: 'Growth', 
              75: 'Razor Leaf', 76: 'Solar Beam', 77: 'Poisonpowder', 78: 'Stun Spore', 79: 'Sleep Powder', 
              80: 'Petal Dance', 81: 'String Shot', 82: 'Dragon Rage', 83: 'Fire Spin', 84: 'Thundershock', 
              85: 'Thunderbolt', 86: 'Thunder Wave', 87: 'Thunder', 88: 'Rock Throw', 89: 'Earthquake', 
              90: 'Fissure', 91: 'Dig', 92: 'Toxic', 93: 'Confusion', 94: 'Psychic', 
              95: 'Hypnosis', 96: 'Meditate', 97: 'Agility', 98: 'Quick Attack', 99: 'Rage', 
              100: 'Teleport', 101: 'Night Shade', 102: 'Mimic', 103: 'Screech', 104: 'Double Team', 
              105: 'Recover', 106: 'Harden', 107: 'Minimize', 108: 'Smokescreen', 109: 'Confuse Ray', 
              110: 'Withdraw', 111: 'Defense Curl', 112: 'Barrier', 113: 'Light Screen', 114: 'Haze', 
              115: 'Reflect', 116: 'Focus Energy', 117: 'Bide', 118: 'Metronome', 119: 'Mirror Move', 
              120: 'Selfdestruct', 121: 'Egg Bomb', 122: 'Lick', 123: 'Smog', 124: 'Sludge', 
              125: 'Bone Club', 126: 'Fire Blast', 127: 'Waterfall', 128: 'Clamp', 129: 'Swift', 
              130: 'Skull Bash', 131: 'Spike Cannon', 132: 'Constrict', 133: 'Amnesia', 134: 'Kinesis', 
              135: 'Softboiled', 136: 'Hi Jump Kick', 137: 'Glare', 138: 'Dream Eater', 139: 'Poison Gas', 
              140: 'Barrage', 141: 'Leech Life', 142: 'Lovely Kiss', 143: 'Sky Attack', 144: 'Transform', 
              145: 'Bubble', 146: 'Dizzy Punch', 147: 'Spore', 148: 'Flash', 149: 'Psywave', 
              150: 'Splash', 151: 'Acid Armor', 152: 'Crabhammer', 153: 'Explosion', 154: 'Fury Swipes', 
              155: 'Bonemerang', 156: 'Rest', 157: 'Rock Slide', 158: 'Hyper Fang', 159: 'Sharpen', 
              160: 'Conversion', 161: 'Tri Attack', 162: 'Super Fang', 163: 'Slash', 164: 'Substitute', 
              165: 'Struggle', 166: 'Sketch', 167: 'Triple Kick', 168: 'Thief', 169: 'Spider Web', 
              170: 'Mind Reader', 171: 'Nightmare', 172: 'Flame Wheel', 173: 'Stnore', 174: 'Curse', 
              175: 'Flail', 176: 'Conversion2', 177: 'Aeroblast', 178: 'Cotton Spore', 179: 'Reversal', 
              180: 'Spite', 181: 'Powder Snow', 182: 'Protect', 183: 'Mach Punch', 184: 'Scary Face', 
              185: 'Faint Attack', 186: 'Sweet Kiss', 187: 'Belly Drum', 188: 'Sludge Bomb', 189: 'Mud-Slap', 
              190: 'Octazooka', 191: 'Spikes', 192: 'Zap Cannon', 193: 'Foresight', 194: 'Destiny Bond', 
              195: 'Perish Song', 196: 'Icy Wind', 197: 'Detect', 198: 'Bone Rush', 199: 'Lock-On', 
              200: 'Outrage', 201: 'Sandstorm', 202: 'Giga Drain', 203: 'Endure', 204: 'Charm', 
              205: 'Rollout', 206: 'False Swipe', 207: 'Swagger', 208: 'Milk Drink', 209: 'Spark', 
              210: 'Fury Cutter', 211: 'Steel Wing', 212: 'Mean Look', 213: 'Attract', 214: 'Sleep Talk', 
              215: 'Heal Bell', 216: 'Return', 217: 'Present', 218: 'Frustration', 219: 'Safeguard', 
              220: 'Pain Split', 221: 'Sacred Fire', 222: 'Magnitude', 223: 'Dynamicpunch', 224: 'Megahorn', 
              225: 'Dragonbreath', 226: 'Baton Pass', 227: 'Encore', 228: 'Pursuit', 229: 'Rapid Spin', 
              230: 'Sweet Scent', 231: 'Iron Tail', 232: 'Metal Claw', 233: 'Vital Throw', 234: 'Morning Sun', 
              235: 'Synthesis', 236: 'Moonlight', 237: 'Hidden Power', 238: 'Cross Chop', 239: 'Twister', 
              240: 'Rain Dance', 241: 'Sunny Day', 242: 'Crunch', 243: 'Mirror Coat', 244: 'Psych Up', 
              245: 'Extremespeed', 246: 'Ancientpower', 247: 'Shadow Ball', 248: 'Future Sight', 249: 'Rock Smash', 
              250: 'Whirlpool', 251: 'Beat Up', 252: '[blank]', 253: '999ZAA', 254: '[glitchy]', 255: '[glitchy]'}

def find_move_name(move_id):
    """
    Given a move ID, return the corresponding move name from the move_dict.
    """
    return move_dict.get(move_id, "Unknown Move")

class Move:
    def __init__(self, id, move_type, power, accuracy, move_pp, attack_type, description=""):
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
        self._data = {
            "id": id,
            "name" : find_move_name(id),
            "move_type": move_type,
            "power": power,
            "accuracy": accuracy,
            "move_pp": move_pp,
            "attack_type": attack_type,
            "description": description,
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
        return f"Move({self._data})"

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

# Example object creation
flamethrower = Move(
    id=53,
    move_type="Fire",
    power=90,
    accuracy=100,
    move_pp=15,
    attack_type="Special",
    description="A powerful fire attack that may inflict a burn."
)

# Accessing as a dictionary
print(flamethrower["name"])         # Output: Flamethrower
print(flamethrower["description"])  # Output: A powerful fire attack that may inflict a burn.

# Setting a new value
flamethrower["power"] = 95
print(flamethrower["power"])        # Output: 95

# Iterating over keys
for key in flamethrower:
    print(key, flamethrower[key])

# Viewing all items
print(flamethrower.items())

# Printing the object to see its details
#print(flamethrower)

"""
class Move:
    def __init__(self, name, move_type, power, accuracy, move_pp, attack_type, description):
        ""
        Initialize a new Move object.

        :param name: Name of the move (str)
        :param move_type: Type of the move (e.g., Fire, Water) (str)
        :param power: Power of the move (int)
        :param accuracy: Accuracy percentage of the move (int)
        :param move_pp: Maximum Power Points (PP) for the move (int)
        :param attack_type: Attack type (Physical or Special) (str)
        :param move_description: decsription of the move (str)S
        ""
        self.name = name
        self.move_type = move_type
        self.power = power
        self.accuracy = accuracy
        self.move_pp = move_pp
        self.attack_type = attack_type
        self.description = description

    def __str__(self):
        ""
        String representation of the Move object.
        ""
        return (f"Move(name={self.name}, type={self.move_type}, power={self.power}, "
                f"accuracy={self.accuracy}, PP={self.move_pp}, attack type={self.attack_type}, "
                f"description={self.move_description})")
"""