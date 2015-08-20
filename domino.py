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

def write_data(f):
	global GAME_STATUS, FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST
	all = [GAME_STATUS,FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST]
	f.write(json.dumps(all))

def read_data(f):
	global GAME_STATUS, FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST
	GAME_STATUS, FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST = json.load(f)

def set_bone(board_bone, user_bone, user_list):
	global GAME_STATUS, FULL_LIST, USER_1_LIST, USER_2_LIST, BOARD_LIST

	if board_bone in BOARD_LIST:
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
			#check bone
			if (board_bone // 10 ) == (user_bone % 10):
				BOARD_LIST.insert(0, user_list.pop(user_list.index(user_bone)))	
				print("Bone is OK")
			elif (board_bone // 10 ) == (user_bone // 10):
				rev_user_bone = ((user_bone % 10) * 10 ) + (user_bone//10 )
				BOARD_LIST.insert(0, rev_user_bone)
				user_list.remove(user_bone)			
			else: 
				print ("Bone NOT ok")

		elif len(BOARD_LIST) - 1 == BOARD_LIST.index(board_bone):
			if (board_bone%10) == (user_bone // 10):
				BOARD_LIST.append(user_list.pop(user_list.index(user_bone)))
			elif(board_bone%10) == (user_bone % 10):
				rev_user_bone = ((user_bone % 10) * 10 ) + (user_bone//10 )
				BOARD_LIST.append(rev_user_bone)
				user_list.remove(user_bone)
			else:
				print ("Bone not OK")
		else:
			print("Boars bone position is wrong")


 	# if side == 'L':
 	# 	print("board_bone // 10", board_bone // 10)
 	# 	print("user_bone // 10", user_bone // 10)

 	# 	if (BOARD_LIST[0] // 10 == user_bone // 10) or (BOARD_LIST[0]  10 == user_bone // 10):
 	# 		BOARD_LIST.insert(0, user_list.pop(user_list.index(user_bone)))

if not os.path.isfile(FILE_NAME):
	new_game()
else:
	with open(FILE_NAME, 'r+') as f:
		read_data(f)

if not GAME_STATUS:
	print("We are NOT in GAME!")
	exit()
 
print (sys.argv)
print (sys.argv)

user_name = sys.argv[1]
board_bone = int(sys.argv[2])
user_bone =  int(sys.argv[3])


if user_name == 'user1':
	user_list = USER_1_LIST
	print (user_list)
else:
	user_list = USER_2_LIST
	print (user_list)

return_str = ""

if (board_bone < 0) and (user_bone < 0):
	#game not began yet, we should return user_bone list
	return_str = str(user_list)
else:
	if (board_bone < 0) and ((user_bone >= 0) and (user_bone in user_list)):
	#game not began yet, its a first step
		BOARD_LIST.append(user_list.pop(user_list.index(user_bone)))
	elif (board_bone > 0) and ((user_bone >= 0) and (user_bone in user_list)):
		print("Call set_bone()")
		set_bone(board_bone, user_bone, user_list)
	else:
		print("something goes wrong")






#at the end we should save data to file for the next steps
with open(FILE_NAME, 'w') as f:
	write_data(f)

print("FULL_LIST:", FULL_LIST)
print("BOARD_LIST:", BOARD_LIST)
print("user1:", USER_1_LIST)
print("user2:", USER_2_LIST)


status = 'OK'
return_str = status + return_str
print(return_str, BOARD_LIST)

#parse args
"""
args format:
user_name bone_on_a_board user_bone
"""





"""f = open('domiData', 'r+b')
if f in None:
	print("No file exist")
"""