#!/usr/bin/env python3

import random
import sys
import json
import os.path
import pdb


FULL_LIST = []
USER_NAME_DICT = {}
USER_NAME_LIST = []
BOARD_LIST = []
FILE_NAME = 'dominoData'
FILE_SEPARATOR = '\n'
GAME_STATUS = []
USER_STEP = ""
JSON_OUTPUT = ""
GAME_NAME = ""

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
	USER_STEP, \
	GAME_NAME


	all = [
			GAME_STATUS,\
			FULL_LIST, \
			BOARD_LIST, USER_NAME_LIST, \
			USER_NAME_DICT, \
			USER_STEP, \
			GAME_NAME
			]

	f.write(json.dumps(all))

def read_data():
	global GAME_STATUS,\
	FULL_LIST, BOARD_LIST, USER_NAME_LIST, \
	USER_NAME_DICT, \
	USER_STEP, \
	GAME_NAME
	
	with open(FILE_NAME, 'r+') as f:
		GAME_STATUS, \
		FULL_LIST, \
		BOARD_LIST, \
		USER_NAME_LIST, \
		USER_NAME_DICT, \
		USER_STEP , \
		GAME_NAME = json.load(f)		

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

	return status

def finish_step(return_str):
	#at the end we should save data to file for the next steps
	with open(FILE_NAME, 'w') as f:
		write_data(f)

	exit()


def fill_output_data(user_name, status):
	global USER_NAME_DICT, USER_STEP, JSON_OUTPUT

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
		"state":"",
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
		board_output_list.append(bone_dict.fromkeys(["dom"], str(bone)))
	output_data['board'] = board_output_list

	bone_dict.clear()

	for bone in USER_NAME_DICT[user_name]:
		hand_output_list.append(bone_dict.fromkeys(["dom"], str(bone)))
	output_data['hand'] = hand_output_list

	for name in USER_NAME_DICT.keys():
		if name == user_name:
			pass
		else:
			enemy_dict['name'] = name
			enemy_dict['count'] = str(len(USER_NAME_DICT[name]))
			enemy_dict['step'] = ("Active" if USER_STEP == name else "Passive")
			enemy_output_list.append(enemy_dict.copy())
			enemy_dict.clear()

	JSON_OUTPUT = json.dumps(output_data, indent=4)	
	print (JSON_OUTPUT)


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
		user_name = params_list[1]
		board_bone = int(params_list[2])
		user_bone =  int(params_list[3])


		if len(USER_NAME_DICT) > 4:
			print ("Waiting till more users ")
			return "NOTOK"

		if len(BOARD_LIST) == 0:
			if (board_bone != -1 ):
				print("At first step board bone should be equal to -1 ")
				return "NOTOK"
		elif board_bone not in BOARD_LIST:
				print("Wrong board bone")
				return "NOTOK"
		elif USER_STEP != user_name:
				print("Currently user ", USER_STEP, "on go")
				return "NOTOK"
	
		if user_bone not in USER_NAME_DICT[user_name]:
			print("User bone not in BOARD_LIST")
			return "NOTOK"			

	return "OK"


def check_bone_for_nxt_step(board_bone, user_name):
	step_posible = False
	for user_bone in USER_NAME_DICT[user_name]:
		if len(BOARD_LIST) == 1:
			if (board_bone // 10 ) == (user_bone % 10):
				step_posible = True
				break
				
			elif (board_bone // 10 ) == (user_bone // 10):				
				step_posible = True
				break

			elif (board_bone%10) == (user_bone // 10):
				step_posible = True
				break

			elif (board_bone%10) == (user_bone % 10):
				step_posible = True
				break

		elif 0 == BOARD_LIST.index(board_bone):
			if (board_bone // 10 ) == (user_bone % 10):
				step_posible = True
				break

			elif (board_bone // 10 ) == (user_bone // 10):
				step_posible = True
				break

			else: 
				step_posible = False

		elif len(BOARD_LIST) - 1 == BOARD_LIST.index(board_bone):
			if (board_bone%10) == (user_bone // 10):
				step_posible = True
				break

			elif(board_bone%10) == (user_bone % 10):
				step_posible = True
				break

			else:
				step_posible = False
		else:
			step_posible = False

	return step_posible


def choose_next_user(user_name, next_user):
	global USER_STEP

	step_posible = False
	next_user = USER_NAME_LIST[(USER_NAME_LIST.index(user_name) + 1)%4]	

	while next_user != user_name:
		if len(BOARD_LIST) == 1:
			if check_bone_for_nxt_step(BOARD_LIST[0], next_user):
				step_posible = True
				break	
		elif check_bone_for_nxt_step(BOARD_LIST[0], next_user) or \
			check_bone_for_nxt_step(BOARD_LIST[-1], next_user):
			step_posible = True
			break

		next_user = USER_NAME_LIST[(USER_NAME_LIST.index(next_user) + 1)%4]	
	else:
		pass

	if step_posible:
		USER_STEP = next_user

	return ("OK" if step_posible == True else "NOTOK")




def main_game(params):

	if len(params) != 6 :
		print("Wrong number of parameters")
		return "NOTOK", ""

	state, token, pname, gname, board_bone, user_bone = params

	board_bone = int(board_bone)
	user_bone = int(user_bone)


	if not os.path.isfile(FILE_NAME):
		new_game()
	else:
		read_data()

	#add new user
	if state == "entry":

		#check do we have this user added prev.
		if pname in USER_NAME_LIST:
			print("We already have this user")
			status = "NOTOK"
		elif len(USER_NAME_LIST) >= 4:
			print ("We already have 4 users")
			status = "NOTOK"
		else:
			user_list = []

			for i in range(7):
				user_list.append(FULL_LIST.pop(random.randrange(0,len(FULL_LIST))))

			user_dict = {
				"state":"wait",
				"hand":user_list
					}

			USER_NAME_DICT[pname] = user_dict
			USER_NAME_LIST.append(pname)
	elif state == "wait":
		#
		pass

	elif state == "playboard":

		user_gict = USER_NAME_DICT.get(pname)
		user_list = user_gict['hand']
		print (user_list)
		if USER_STEP == "" and len(BOARD_LIST) == 0:			
			if user_bone == 11:	
				BOARD_LIST.append(user_list.pop(user_list.index(user_bone)))
			else:
				print ("Only 1:1 can start the game")
				status = "NOTOK"
		elif USER_STEP == user_name:	
			status = set_bone(board_bone, user_bone, user_list)		
		else:
			status = "NOTOK"
			print("Currently user ", USER_STEP, "on go")

		# if status == "OK":
		# 	if len(USER_NAME_DICT[user_name]) == 0:
		# 		final_output(user_name)
			

	print(USER_NAME_DICT)

	finish_step("")	

	return state, "sdfghj"


if __name__ == "__main__":
	user_list = []
	status =""

	#trying to read data form file
	if not os.path.isfile(FILE_NAME):
		new_game()
	else:
		read_data()

	status = validate_params(sys.argv)
	if status == "NOTOK":
		user_name = sys.argv[1]
		fill_output_data(user_name, status)
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

		user_list = USER_NAME_DICT.get(user_name)
		if USER_STEP == "" and len(BOARD_LIST) == 0:			
			if user_bone == 11:	
				BOARD_LIST.append(user_list.pop(user_list.index(user_bone)))
			else:
				print ("Only 1:1 can start the game")
				status = "NOTOK"
		elif USER_STEP == user_name:	
			status = set_bone(board_bone, user_bone, user_list)		
		else:
			status = "NOTOK"
			print("Currently user ", USER_STEP, "on go")

		if status == "OK":
			if len(USER_NAME_DICT[user_name]) == 0:
				final_output(user_name)
			
			#choose next user
			next_user = ""
			status = choose_next_user(user_name, next_user)
			

	fill_output_data(user_name, status)
	return_str = status

	finish_step(return_str)


