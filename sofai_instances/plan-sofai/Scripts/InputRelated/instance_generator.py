#
# This Python File generates tot_inst * tot_iter instances of the coininthebox domain
#
# Run it with "python3 instance_generator.py" to generate in the folder  "coinintheboxgen/instances" the instances.
#

import os
import string
from pathlib import Path
import random
import numpy as np

tot_inst = 1000
tot_iter = 10


depth = 2
dynck = "false"

max_agents = 3
min_goals = 1
max_goals = 7
max_nesting = 3
fluents_goal_list = ["tail","opened","in_room_empty","in_room_box","looking"]
list_agents = list(string.ascii_lowercase)


def generate_random_initial_state(tot_agents):

    sample_arr = [True,False]
    agents_pos = np.random.choice(sample_arr, size=tot_agents)
    initial_state = ""

    ####FACTS
    #initial position of each agent
    tmp_agent = 0
    while tmp_agent < tot_agents:
        if (agents_pos[tmp_agent]):
            initial_state += " (in_room_empty " + str(list_agents[tmp_agent])+ ")"
        else:
            initial_state += " (in_room_box " + str(list_agents[tmp_agent])+ ")"
        tmp_agent += 1

    #which agent has the key
    key_agent = random.randint(0, tot_agents-1)
    initial_state += " (has_key " + str(list_agents[key_agent])+ ")"

    #The coin state
    coin_state = bool(random.getrandbits(1)) #If true then the coin is heads up
    if(coin_state):
        initial_state += " (tail)"
#    else:
#        initial_state += " (-tail)"

    #The box state
    box_state = bool(random.getrandbits(1)) #If true then the box is open
    if(box_state):
        initial_state += " (opened)"
#    else:
#        initial_state += " (-opened)"

    #The looking agents (at least one)
    agents_look = np.random.choice(sample_arr, size=tot_agents)
    none_looking = True
    tmp_agent = 0
    while tmp_agent < tot_agents:
        if (agents_look[tmp_agent]):
            initial_state += " (looking " + str(list_agents[tmp_agent])+ ")"
            none_looking = False
#        else:
#            initial_state += " (in_room_box " + str(list_agents[tmp_agent])+ ")"
        tmp_agent += 1

    if (none_looking):
        look_agent = random.randint(0, tot_agents-1)
        initial_state += " (looking " + str(list_agents[look_agent])+ ")"


    ####COMMON KNOWLEDGE ABOUT THE FACTS
    common_knowledge = " (["
    tmp_agent = 0
    while tmp_agent < tot_agents:
        common_knowledge += str(list_agents[tmp_agent])
        if (tmp_agent+1 < tot_agents):
            common_knowledge += " "
        tmp_agent += 1
    common_knowledge += "]"

    #initial position of each agent
    tmp_agent = 0
    while tmp_agent < tot_agents:
        if (agents_pos[tmp_agent]):
            initial_state += common_knowledge + "(in_room_empty " + str(list_agents[tmp_agent])+ "))"
            initial_state += common_knowledge + "(-in_room_box " + str(list_agents[tmp_agent])+ "))"
        else:
            initial_state += common_knowledge + "(in_room_box " + str(list_agents[tmp_agent])+ "))"
            initial_state += common_knowledge + "(-in_room_empty " + str(list_agents[tmp_agent])+ "))"
        tmp_agent += 1

    #which agent has the key
    tmp_agent = 0
    while tmp_agent < tot_agents:
        if (tmp_agent == key_agent):
            initial_state += common_knowledge + "(has_key " + str(list_agents[tmp_agent])+ "))"
        else:
            initial_state += common_knowledge + "(-has_key " + str(list_agents[tmp_agent])+ "))"
        tmp_agent += 1

    #The box state
    if(box_state):
        initial_state += common_knowledge + "(opened))"
    else:
        initial_state += common_knowledge + "(-opened))"


    #The looking agents (at least one)
    tmp_agent = 0
    if (none_looking):
        while tmp_agent < tot_agents:
            if (tmp_agent == look_agent):
                initial_state += common_knowledge + "(looking " + str(list_agents[tmp_agent])+ "))"
            else:
                initial_state += common_knowledge + "(-looking " + str(list_agents[tmp_agent])+ "))"
            tmp_agent += 1
    else:
        while tmp_agent < tot_agents:
            if (agents_look[tmp_agent]):
                initial_state += common_knowledge + "(looking " + str(list_agents[tmp_agent])+ "))"
            else:
                initial_state += common_knowledge + "(-looking " + str(list_agents[tmp_agent])+ "))"
            tmp_agent += 1

    return initial_state

def generate_random_goal_state(tot_agents):
    goals_number = random.randint(min_goals, max_goals)
    found_goals = 0
    goal = ""
    while found_goals < goals_number:
        subgoal = " ("
        nesting = random.randint(0, max_nesting)
        nest_count = 0
        while nest_count < nesting:
            ag = random.randint(0, tot_agents-1)
            subgoal += "[" + str(list_agents[ag])+ "]"
            nest_count += 1
            if (nest_count == nesting):
                subgoal += "("

        selected_fluent = random.randint(0, (len(fluents_goal_list)-1))
        if (selected_fluent == 0 and nesting == 0):
            found_goals -=1
            subgoal = ""
        else:
            if (selected_fluent < 2):
                fluent = fluents_goal_list[selected_fluent]
            else:
                fluent = fluents_goal_list[selected_fluent] + " " + str(list_agents[random.randint(0, tot_agents-1)])

            if(bool(random.getrandbits(1))):
                subgoal += fluent + ")"
            else:
                subgoal += "-" + fluent + ")"

            if nesting > 0:
                subgoal += ")"

        goal += subgoal
        found_goals += 1

    return goal

if __name__ == '__main__':

    l_inst = len(str(tot_inst))
    l_iter = len(str(tot_iter))


    n_inst = 0

    dir_path = "../../coinintheboxgen/instances/"
    os.makedirs(dir_path, exist_ok=True)


    while n_inst < tot_inst:

        n_iter = 0

        tot_agents = random.randint(2, max_agents)
        initial_state = generate_random_initial_state(tot_agents)

        while n_iter < tot_iter:
            #string_n_inst = "{:0"+l_inst+"d}".format(n_inst)
            string_n_inst = str(n_inst).zfill(l_inst-1)
            #string_n_iter = "{:0"+l_iter+"d}".format(n_iter)
            string_n_iter = str(n_iter).zfill(l_iter-1)

            gen_filename = dir_path + "pb" + string_n_inst + "_" + string_n_iter + ".epddl"
            with open(gen_filename, 'w') as gen_f:
                print("(define (problem pb" + string_n_inst + "_" + string_n_iter + ")", file=gen_f)

                print("  (:domain coininthebox)", file=gen_f)

                print("  (:agents",end = '', file=gen_f)
                print_agents = 0
                while print_agents < tot_agents:
                    print(" " + str(list_agents[print_agents]),end = '', file=gen_f)
                    print_agents += 1
                print(")", file=gen_f)

                print("  (:depth " + str(depth) + ")", file=gen_f)

                print("  (:dynck " + str(dynck) + ")", file=gen_f)

                print("  (:init " + str(initial_state) + ")", file=gen_f)

                print("  (:goal", str(generate_random_goal_state(tot_agents)) + ")", file=gen_f)

                print(")", file=gen_f)

            n_iter +=1


        n_inst += 1
