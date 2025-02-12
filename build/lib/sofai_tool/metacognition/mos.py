
import time
import os
import json
import subprocess
import re
import csv
from pathlib import Path
import sys
import pprint
from time import gmtime, strftime
import random
import traceback
import logging

global timerParsing
global timerSOFAI


### Type of Systems
systemALL = -1              # Constant that represents both System-1 and System-2
systemONE = 1               # Constant that represents only System-1
systemTWO = 2   

output_folder = "output/"
dbFolder = "db/"
global experience_file
experience_file = None
jsonAllSolFilename = "allS1Solutions.json"
maxExperience = 1000

'''Function that sets up the environment by creating some necessary folders'''
def createFolders(jsonFilename, new_run):
    global experience_file
    # check if this file exists and remove it and create it again 
    # if os.path.exists(dbFolder + jsonFilename):
    #     os.remove(dbFolder + jsonFilename)
    experience_file = dbFolder + jsonFilename
    Path(output_folder).mkdir(parents=True,exist_ok=True)
    # Path(output_folderPl1).mkdir(parents=True,exist_ok=True) # what is the use of this?
    ### Creating the memory file if it doesn't exist
    
    Path(dbFolder).mkdir(parents=True,exist_ok=True)

    # if it is a new run, then we delete if the file exists
    if new_run:
        if os.path.exists(experience_file):
            os.remove(experience_file)
    if not os.path.isfile(experience_file):
        f = open(experience_file, "w")
        f.write("{\n\"size_limit\": 1000,\n\"cases\":{\n}\n}")
        f.close

def memorize_solution(solver, system, name, timerComputation, difficulty, continue_solve=False, temp_solve=False):
    try:
        memory_file = open(experience_file)
    except:
        createFolders()
        memory_file = open(experience_file)

    totalTIME = time.time()-timerComputation


    data = json.load(memory_file)

    if ('cases' not in data.keys()) or (len(data['cases']) == 0):
        index = 0
    else:
        index = max( [int(k) for k in data['cases'].keys()] )

    index += 1

    #jsonformat established here

    data['cases'][str(index)] = {}
    data['cases'][str(index)]['name'] = name # how?
    data['cases'][str(index)]['difficulty'] = difficulty # how?
    data['cases'][str(index)]['system'] = system
    data['cases'][str(index)]['confidence'] = solver.confidence
    data['cases'][str(index)]['correctness'] = solver.correctness
    data['cases'][str(index)]['solving_time'] = solver.running_time
    data['cases'][str(index)]['total_time'] = totalTIME

    #init,goal = getStates.States(problemFile) #reading initial and goal states from problem file

    data['cases'][str(index)]['problem'] = name+".pickle" # how?
    data['cases'][str(index)]['solution'] = solver.solution



    if not temp_solve:
        json_object = json.dumps(data,indent=4)
        # writing dictionary data into json file
        with open(experience_file,"w") as out:
            out.write(json_object)
    
    if continue_solve:
        return
    
    print(f"Solution found by System {system}!\
            \n\tSOLUTION:{solver.solution}\
            \n\tCORRECTNESS: {solver.correctness}\
            \n\tSOLVER TIME: {solver.running_time}s\
            \n\tSOFAI TIME: {totalTIME}s")


    #utilities.end_computation(name,timerComputation,True)

'''Utility function that counts how many solutions have been solved by System 1 in the experience'''
def count_solved_instances(system):
    dbFilename = experience_file
    matchCount = 0
    totalCorrectness = 0

    # Opening JSON file
    try:
        f = open(dbFilename)
        # returns JSON object as a dictionary
        data = json.load(f)

        index = len(data['cases'])
        count = 0
        while (index > 0) and (count < maxExperience):
            # if(data['cases'][str(index)]['name'] == name):
                #planner == systemALL means that we accept all the planners
            if(int(data['cases'][str(index)]['system']) == system or system == systemALL):
                # if(int(data['cases'][str(index)]['planner']) == planner or planner == plannerALL):
                matchCount += 1
            index -= 1
            count += 1

        return matchCount
    except IOError:
        return 0
    
'''Utility function that return the correctness (average) of System 1 in the last 'sliding window' instances'''
def get_avg_corr(system,slidingWindow):
    dbFilename = experience_file
    matchCount = 0
    totalCorrectness = 0

    # Opening JSON file
    f = open(dbFilename)
    # returns JSON object as a dictionary
    data = json.load(f)

    index = len(data['cases'])
    count = 0
    while (index > 0) and (count < maxExperience):
        # if(data['cases'][str(index)]['name'] == name):
            #planner == systemALL means that we accept all the planners
        if(int(data['cases'][str(index)]['system']) == system or system == systemALL):
            # if(int(data['cases'][str(index)]['planner']) == planner or planner == plannerALL):
            if (matchCount < slidingWindow):
                matchCount += 1
                totalCorrectness += float(data['cases'][str(index)]['correctness'])
            else:
                index = 0
        index -= 1
        count += 1


    if matchCount > 0:
        return (totalCorrectness/matchCount)
    else:
        return 0

import json

def estimate_time_consumption(problem, difficulty):
    dbFilename = experience_file
    range_limit = 100
    timer_computation_consumption = 0
    match_count = 0

    try:
        with open(dbFilename, 'r') as db:
            data = json.load(db)

            for case_id, case_data in data['cases'].items():
                if case_data['system'] == 2: #We only use the difficulty for S2 porpouses for now
                    if case_data['problem'] == problem:
                        case_difficulty = float(case_data['difficulty'])
                        if (case_difficulty < (difficulty + range_limit)) and (case_difficulty > (difficulty - range_limit)):
                            match_count += 1
                            timer_computation_consumption += float(case_data['solving_time'])

    except IOError:
        match_count = 0

    if match_count > 0:
        return timer_computation_consumption / match_count
    else:
        no_match_consumption = 5
        return no_match_consumption