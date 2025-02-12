#
# This Python File generates the testbed for Plansformer from the results file
#
# Run it with "python3 plansformer_gen.py" to generate the results, considering the "instances_folder" and "res_filename"
#

import os
import json
import subprocess
import re
import csv
from pathlib import Path
import sys
import pprint
import time
import random

def getVarFromFile(filename,varname):
    with open(filename) as myfile:
        for line in myfile:
            if ":"+varname in line:
                line = re.sub(r';.*$', '', line)
                discard, var = line.partition(":"+varname)[::2]
                var = var.replace(")", "")
                myfile.close()
                return var.strip()
        raise Exception('Missing variable named '+ varname)
    raise Exception('Missing file named '+ filename)

def getRawVarFromFile(filename,varname):
    with open(filename) as myfile:
        for line in myfile:
            if ":"+varname in line:
                line = re.sub(r';.*$', '', line)
                discard, var = line.partition(":"+varname)[::2]
                myfile.close()
                return var
        raise Exception('Missing variable named '+ varname)
    raise Exception('Missing file named '+ filename)

def cleanString(mystring):
    mystring = re.sub("\)\s*\(", ", ", mystring)

    mystring = mystring.strip()
    mystring = mystring[1:]
    mystring = mystring[:-2]
    return mystring

def getVarFromLine(line,varname):
#    print("Cond is </"+varname+">")
    if "</"+varname+">" in line:
        line = re.sub(r'.*</'+varname+'>([^<]+)</>.*',r'\1', line)
        return line.strip()
    return ''


if __name__ == '__main__':

    instances_folder = "../../Input/coininthebox_closed/instances"
    act_string = "<ACTION> move_to_box <ACT_TYPE> ontic <PRE> [?ag](in_room_empty ?ag), in_room_empty ?ag <EFFECT> in_room_box ?ag, -in_room_empty ?ag <ACTION> move_to_empty <ACT_TYPE> ontic <PRE> [?ag](in_room_box ?ag), in_room_box ?ag <EFFECT> in_room_empty ?ag, -in_room_box ?ag <ACTION> open <ACT_TYPE> ontic <PRE> [?ag](has_key ?ag), has_key ?ag, in_room_box ?ag <EFFECT> opened <ACTION> close <ACT_TYPE> ontic <PRE> [?ag](has_key ?ag), has_key ?ag, in_room_box ?ag <EFFECT> -opened <ACTION> signal <ACT_TYPE> ontic <PRE> [?ag1](looking ?ag1), [?ag2](not (looking ?ag2)) <EFFECT> looking ?ag2 <ACTION> peek <ACT_TYPE> sensing <PRE> [?ag](opened), [?ag](looking ?ag), looking ?ag, opened, in_room_box ?ag <EFFECT> tail <ACTION> distract <ACT_TYPE> ontic <PRE> [?ag1](looking ?ag1), [?ag2](looking ?ag2) <EFFECT> not (looking ?ag2) <ACTION> announce_room_box <ACT_TYPE> announcement <PRE> [?ag](tail), tail, in_room_box ?ag <EFFECT> tail <ACTION> announce_room_empty <ACT_TYPE> announcement <PRE> [?ag](tail), tail, in_room_empty ?ag <EFFECT> tail"
    #act_string = ""
    outfile = "testbed_new.csv"
    res_filename = "../../Output/SOL/solSys2_new.txt"
    #print("ModName is " + modfilename + " and number is " +  str(instance_number))
    count = 0
    with open(outfile, 'w') as f:
        print("DomainProblem,Plan", end='\n', file=f)
        with open("out.tmp", 'w') as out:

            for filename in os.listdir(instances_folder):
                readingFile = os.path.join(instances_folder, filename)
                # checking if it is a file
                if os.path.isfile(readingFile):
                    init = getRawVarFromFile(readingFile,"init")
                    init = cleanString(init)

                    goal = getRawVarFromFile(readingFile,"goal")
                    goal = cleanString(goal)

                    print("\""+"<GOAL>", end='', file=f)
                    print(goal, end='', file=f)
                    print("<INIT>", end='', file=f)
                    print(init, end='', file=f)

                    print(act_string, end='\",', file=f)

                    res_file = open(res_filename,'r')
                    res_file_lines = res_file.readlines()
                    neverfound = True
                    for line in res_file_lines:
                        to_check = filename[:-6]
                        to_check = re.sub("(pb)(0*)(\d+)(_)(0*)(\d+)", r'\1\3\4\6', to_check)
                        to_check = "</pro>" + to_check + "</>"
                        if to_check in line:
                            neverfound = False
                            plan = getVarFromLine(line, "sol")
                            plan = plan.replace("[","")
                            plan = plan.replace("]","")
                            plan = plan.replace("\'","")

                    if not plan == "":
                        print("\""+plan+"\"", end='\n', file=f)
                        count = count +1
                    else:
                        print("NOT FOUND", end='\n', file=f)
                        print("Input/coininthebox/instances/" + filename,file=out)
                    if neverfound:
                        print(to_check + "NOT EXISTENT", end='\n', file=f)

    print ("Count is " + str(count))
