import random
import sys
import json
import os.path

#RIGHT_END
#LEFT_END
FULL_LIST = []
USER_1_LIST = []
USER_2_LIST = []
BOARD_LIST = []
FILE_NAME = 'dominoData'
FILE_SEPARATOR = '\n'
GAME_STATUS = []

"""
File format:
0/1 - game condition (0 - not started, 1 - in progress)
[]  - FULL_LIST
[]	- USER_1_LIST
[]	- USER_2_LIST
[]	- BOARD_LIST
"""
def new_game():
	global FULL_LIST, USER_1_LIST, USER_2_LIST, GAME_STATUS

	GAME_STATUS = [1]
	for i in range(7):
		FULL_LIST +=[b for b in range((i*10)+i,(i*10) + 7)] 

	#print (FULL_LIST, len(FULL_LIST))

	for i in range(7):
		USER_1_LIST.append(FULL_LIST.pop(random.randrange(0,len(FULL_LIST))))

	for i in range(7):
		USER_2_LIST.append(FULL_LIST.pop(random.randrange(0,len(FULL_LIST))))

	with open(FILE_NAME, 'w') as f:
		write_data(f)	

def write_data(f):
	global GAME_STATUS, FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST
	all = [GAME_STATUS,FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST]
	f.write(json.dumps(all))

def read_data(f):
	global GAME_STATUS, FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST
	GAME_STATUS, FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST = json.load(f)
	print ("reeded list", FULL_LIST, len(FULL_LIST))
	
def set_bone(board_bone, user_bone, side, user_list):
	global GAME_STATUS, FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST

	if side == 'L':
		print("board_bone // 10", board_bone // 10)
		print("user_bone // 10", user_bone // 10)

		if (BOARD_LIST[0] // 10 == user_bone // 10) or (BOARD_LIST[0]  10 == user_bone // 10):
			BOARD_LIST.insert(0, user_list.pop(user_list.index(user_bone)))

if not os.path.isfile(FILE_NAME):
	new_game()
else:
	with open(FILE_NAME, 'r+') as f:
		read_data(f)

if not GAME_STATUS:
	print("We are NOT in GAME!")
	exit()
 
print (sys.argv)

user_name = sys.argv[1]
board_bone = int(sys.argv[2])
user_bone =  int(sys.argv[3])
side = sys.argv[4]

if user_name == 'user1':
	user_list = USER_1_LIST
	print (user_list)
else:
	user_list = USER_2_LIST
	print (user_list)


if board_bone == -1:
	#game not began yet, its a first step
	if user_bone in user_list:
		BOARD_LIST.append(user_list.pop(user_list.index(user_bone)))
		print("BOARD_LIST:", BOARD_LIST)
		print("user_list:", user_list)
#else:
	#check is current step valid




#at the end we should save data to file for the next steps
with open(FILE_NAME, 'w') as f:
	write_data(f)


status = 'OK'

print(status, BOARD_LIST)

#parse args
"""
args format:
user_name bone_on_a_board user_bone
"""





"""f = open('domiData', 'r+b')
if f in None:
	print("No file exist")
"""