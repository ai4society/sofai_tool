#
# This Python File generates a modfied instance, with the extra goal "(not(opened)))", from the input one
#
# Run it with "python3 instance_modifier.py filename" to generate the modfied filename in "coininthebox-mod/instances".
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

if __name__ == '__main__':

    filename = sys.argv[1]

    agents = getVarFromFile(filename,"agents").split()
    depth = getRawVarFromFile(filename,"depth")
    dynck = getRawVarFromFile(filename,"dynck")
    init = getRawVarFromFile(filename,"init")
    goal = getRawVarFromFile(filename,"goal")

    #print(str(agents))

    #
    path, name = os.path.split(filename)
    #print("Name is " + name)

    instance_number = int((re.sub(r'(pb)(\d+)(\_)(\d+\.epddl)', r'\2',name)))
    iter_number = int((re.sub(r'(pb)(\d+)(\_)(\d+)(\.epddl)', r'\4',name)))

    #print("Name is " + name + " and number is " +  str(instance_number))
    instance_number += 0

    modfilename = "../../Input/coininthebox-mod/instances/pb" + str(instance_number) + "_" + str(iter_number) + ".epddl"
    #print("ModName is " + modfilename + " and number is " +  str(instance_number))

    with open(modfilename, 'w') as f:
        print("(define (problem pb" + str(instance_number)+ "_" + str(iter_number)+ ")", file=f)
        print("  (:domain coininthebox)", file=f)
        print("  (:agents",end = '', file=f)
        for agent in agents:
            print(" " + str(agent),end = '', file=f)
        print(")", file=f)
        print("  (:depth "+str(depth), end='', file=f)
        print("  (:dynck "+str(dynck), end='', file=f)
        print("  (:init "+str(init), end='', file=f)
        print("  (:goal ", end='', file=f)
        print("(not(opened))", end='', file=f)
        print(" " + goal, end='', file=f)
        print(")", file=f)
