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




#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is interface function between game View and game Control
# Input strings:
#        state - current state from which request passed: entry, wait, playboard, statistic) [mandatory]
#        token - game token
#        pname - player name
#        gname - game name
#        tname - team name
#        bb    - board bone
#        hb    - hand bone
# Output strings:
#        state - generated new state
#        json_out - is defined in example below
def get_game_data(state, token, pname, gname, tname, bb, hb):
#TODO
    json_out = '{\
                "status":"ok",\
                "state":"entry",\
                "token":"381290380123812983012830",\
                "user_name":"Vasya",\
                "game_name":"Super puper mega game",\
                "team_name":"Awesome team",\
                "step":"active",\
                "board":[{"dom":"00"},{"dom":"01"},{"dom":"11"},{"dom":"21"},{"dom":"23"},{"dom":"34"},{"dom":"44"},{"dom":"46"},\
                         {"dom":"00"},{"dom":"01"},{"dom":"11"},{"dom":"21"},{"dom":"23"},{"dom":"34"},{"dom":"44"},{"dom":"46"},\
                         {"dom":"53"},{"dom":"01"},{"dom":"62"},{"dom":"12"},{"dom":"23"},{"dom":"34"},{"dom":"42"},{"dom":"46"}\
                        ],\
                "hand":[{"dom":"33"},{"dom":"45"},{"dom":"36"},{"dom":"22"}],\
                "enemy":[{"name":"John", "count":"7", "step":"passive"},\
                         {"name":"Кузнечик", "count":"5", "step":"passive"},\
                         {"name":"Larisa", "count":"3", "step":"passive"}],\
                "stat":"Long string (plain text) with game statisitc, for now:)"\
                };'

    state = "entry"
    return (state, json_out)
