import retro
import retro.data  
import json
import struct
import sys
#state = retro.State('Battle')
#action = []
#env = retro.make(game='PokemonSilver-GbColor', state='Battle')
#env.reset()
#done = False




game='PokemonSilver-GbColor'
data_path = "/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor/data.json"
scenario_path = "/home/borg/vretro/lib/python3.12/site-packages/retro/data/stable/PokemonSilver-GbColor/scenario.json"
env = retro.make(game, 'Battle.state')
env.reset()

done = False
i = 0
while not done:
    env.render()
    action = [0,0,0,0,0,0,0,0,0,0,0,0]
    env.step(action)

    obs, _, done, _, info = env.step(action)
    print("Info ", info['HP']) 
    i = i+1
    if i is 3:
        done = True

#data = open(data_path, "r")
#lines = data.readlines()
#print(lines)
#with open(data_path, 'r') as file:
#    env.data = json.load(file)


#hp_address = env.data["info"]["HP"]["address"]
#hp_type = env.data["info"]["HP"]["type"]



#hp_bytes = env.get_ram
#hp_value = struct.unpack(hp_type, hp_bytes)[0]


#print(env.get_ram())

#while True:
#     _info = env.step(env.action_space.sample())
     

#print(retro.data.list_games())

