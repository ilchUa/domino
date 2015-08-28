# This is interface function between game View and game Control
# Input strings:
#        state - current state from which request passed: entry, wait, playboard, statistic) [mandatory]
#        token - game token
#        pname - player name
#        gname - game name
#        bb    - board bone
#        hb    - hand bone
# Output strings:
#        state - generated new state
#        json_out - will be defined to every state
from domino import main_game
import pdb
def get_game_data(state, token, pname, gname, bb, hb):
	json_out = ""
	params = [state, token, pname, gname, bb, hb]
	state, json_out = main_game(params)
	#print(state)
	return state, json_out

#pdb.set_trace()
state, json_out = get_game_data("entry","","user1", "gam1", "12", "11")
print(state, json_out)

