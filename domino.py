import random
import sys
import json
import os.path

FULL_LIST = []
USER_NAME_DICT = {}
USER_NAME_LIST = []
BOARD_LIST = []
FILE_NAME = 'dominoData'
FILE_SEPARATOR = '\n'
GAME_STATUS = []
USER_STEP = ""

def new_game():
	global GAME_STATUS,\
	FULL_LIST	

	GAME_STATUS = [1]
	for i in range(7):
		FULL_LIST +=[b for b in range((i*10)+i,(i*10) + 7)] 

def write_data(f):
	global GAME_STATUS,\
	FULL_LIST, \
	BOARD_LIST, USER_NAME_LIST, \
	USER_NAME_DICT, \
	USER_STEP

	all = [
			GAME_STATUS,\
			FULL_LIST, \
			BOARD_LIST, USER_NAME_LIST, \
			USER_NAME_DICT, \
			USER_STEP
			]

	f.write(json.dumps(all))

def read_data():
	global GAME_STATUS,\
	FULL_LIST, BOARD_LIST, USER_NAME_LIST, \
	USER_NAME_DICT, \
	USER_STEP
	
	with open(FILE_NAME, 'r+') as f:
		GAME_STATUS, \
		FULL_LIST, \
		BOARD_LIST, \
		USER_NAME_LIST, \
		USER_NAME_DICT, \
		USER_STEP = json.load(f)		

def set_bone(board_bone, user_bone, user_list):
	global BOARD_LIST

	status = "OK"
	if len(BOARD_LIST) == 1:
		if (board_bone // 10 ) == (user_bone % 10):
			BOARD_LIST.insert(0, user_list.pop(user_list.index(user_bone)))	
			
		elif (board_bone // 10 ) == (user_bone // 10):
			rev_user_bone = ((user_bone % 10) * 10 ) + (user_bone//10 )
			BOARD_LIST.insert(0, rev_user_bone)
			user_list.remove(user_bone)

		elif (board_bone%10) == (user_bone // 10):
			BOARD_LIST.append(user_list.pop(user_list.index(user_bone)))

		elif (board_bone%10) == (user_bone % 10):
			rev_user_bone = ((user_bone % 10) * 10 ) + (user_bone//10 )
			BOARD_LIST.append(rev_user_bone)
			user_list.remove(user_bone)

	elif 0 == BOARD_LIST.index(board_bone):
		if (board_bone // 10 ) == (user_bone % 10):
			BOARD_LIST.insert(0, user_list.pop(user_list.index(user_bone)))	
		elif (board_bone // 10 ) == (user_bone // 10):
			rev_user_bone = ((user_bone % 10) * 10 ) + (user_bone//10 )
			BOARD_LIST.insert(0, rev_user_bone)
			user_list.remove(user_bone)			
		else: 
			status = "NOTOK"

	elif len(BOARD_LIST) - 1 == BOARD_LIST.index(board_bone):
		if (board_bone%10) == (user_bone // 10):
			BOARD_LIST.append(user_list.pop(user_list.index(user_bone)))
		elif(board_bone%10) == (user_bone % 10):
			rev_user_bone = ((user_bone % 10) * 10 ) + (user_bone//10 )
			BOARD_LIST.append(rev_user_bone)
			user_list.remove(user_bone)
		else:
			status = "NOTOK"
	else:
		status = "NOTOK"


def finish_step(return_str):
	#at the end we should save data to file for the next steps
	with open(FILE_NAME, 'w') as f:
		write_data(f)

	exit()

 	# if side == 'L':
 	# 	print("board_bone // 10", board_bone // 10)
 	# 	print("user_bone // 10", user_bone // 10)

 	# 	if (BOARD_LIST[0] // 10 == user_bone // 10) or (BOARD_LIST[0]  10 == user_bone // 10):
 	# 		BOARD_LIST.insert(0, user_list.pop(user_list.index(user_bone)))



def fill_output_data(user_list, user_name, status):
	global USER_NAME_DICT

	board_output_list = []
	hand_output_list = []
	bone_dict = {}
	enemy_output_list = []
	enemy_dict = {
		"name":"",
		"count":"",
		"step":""
	}

	#OUtput structure :
	output_data = {
		"status":"",
		"token":"0",
		"user_name":"",
		"step":"",
		"board":board_output_list,
		"hand":hand_output_list,
		"enemy":enemy_output_list
	}

	#Fill output dict
	output_data['status'] = status
	output_data['user_name'] = user_name
	output_data['step'] = "active"

	#fill board_output_list
	for bone in BOARD_LIST:
		board_output_list.append(bone_dict.fromkeys(["dom"], bone))
	output_data['board'] = board_output_list

	bone_dict.clear()

	for bone in user_list:
		hand_output_list.append(bone_dict.fromkeys(["dom"], bone))
	output_data['hand'] = hand_output_list

	for name in USER_NAME_DICT.keys():
		if name == user_name:
			pass
		else:
			enemy_dict['name'] = name
			enemy_dict['count'] = len(USER_NAME_DICT[name])
			enemy_dict['step'] = ("Active" if USER_STEP == name else "Passive")
			enemy_output_list.append(enemy_dict.copy())
			enemy_dict.clear()

	print("output_data:")
	print (json.dumps(output_data, indent=4))

def validate_params(params_list):
	global USER_NAME_DICT, BOARD_LIST

	if (len(params_list) != 2) and (len(params_list) != 4):
		print("Wrong number of parameters")
		return "NOTOK"

	if (len(params_list) == 2):
		if (len(USER_NAME_DICT) >= 4):
			print("Error, we already has a 4 users", file=sys.stderr)
			return "NOTOK"

		if sys.argv[1] in USER_NAME_DICT.keys():
			print("This user is already exist")
			return "NOTOK"
	
	elif len(params_list) == 4:
		user_name = sys.argv[1]
		board_bone = int(sys.argv[2])
		user_bone =  int(sys.argv[3])

		if len(USER_NAME_DICT) > 4:
			print ("Waiting till more users ")
			return "NOTOK"

		if len(BOARD_LIST) == 0:
			if (board_bone != -1 ):
				print("At first step board bone should be equal to -1 ")
				return "NOTOK"
		else:
			if board_bone not in BOARD_LIST:
				print("Wrong board bone")
				return "NOTOK"
	
		if user_bone not in USER_NAME_DICT[user_name]:
			print("User bone not in BOARD_LIST")
			return "NOTOK"			

	return "OK"

is_ok = True
user_list = []
status =""

# if validate

# user_list = []
# user_name = sys.argv[1]
# board_bone = int(sys.argv[2])
# user_bone =  int(sys.argv[3])

#trying to read data form file

if not os.path.isfile(FILE_NAME):
	new_game()
else:
	read_data()

status = validate_params(sys.argv)
if status == "NOTOK":
	finish_step(status)

if len(sys.argv) == 2:
	#Adding a new user
	user_list = [] 
	user_name = sys.argv[1]

	for i in range(7):
		user_list.append(FULL_LIST.pop(random.randrange(0,len(FULL_LIST))))

	USER_NAME_DICT[user_name] = user_list
	USER_NAME_LIST.append(user_name)
	status = "OK"	
	
elif len(sys.argv) == 4:

	user_name = sys.argv[1]
	board_bone = int(sys.argv[2])
	user_bone =  int(sys.argv[3])
	#main game func

	if USER_STEP == "" and len(BOARD_LIST) == 0:	
		user_list = USER_NAME_DICT.get(user_name)
		if user_bone == 11:
			#if (board_bone < 0) and ((user_bone >= 0) and (user_bone in user_list)):
			#game not began yet, its a first step
				#if user_bone 
			BOARD_LIST.append(user_list.pop(user_list.index(user_bone)))
		else:
			print ("Only 1:1 can start the game")
			status = "NOTOK"
	elif USER_STEP == user_name:
		
		status = set_bone(board_bone, user_bone, user_list)
		# USER_STEP = [(USER_NAME_LIST.index(USER_STEP) + 1)%4]
	else:
		print("Currently user ", USER_STEP, "on in action")

		

fill_output_data(user_list, user_name, status)
return_str = status
finish_step(return_str)



#parse args
"""
args format:
user_name bone_on_a_board user_bone
"""





"""f = open('domiData', 'r+b')
if f in None:
	print("No file exist")
"""