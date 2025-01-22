global timerTotal
import time
timerTotal = time.time()

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


from Planners.New_PlansformerS1 import mode0 as newPlansformer_s1

from Planners.PDDL_parser import classical_parser
from Planners.PDDL_parser import SubgoalCompleteness

from . import utilities
scripts_folder = "Scripts/"


import sofai_tool as sofai

class CustomSystem1Solver(sofai.System1Solver):
    def solve(self, problem_id):
        
        domain,problem=utilities.split_names(problem_id)
        
        try:
            tens_confidence, plan = newPlansformer_s1.solve(domain,problem,0)
        except Exception as e:
            logging.error(traceback.format_exc())
            raise Exception("System-1 encountered some errors.")

        confidence = float(utilities.tensor_clean(tens_confidence))
        sol = ""
        first_act = True
        for act in plan:
            if first_act:
                sol = act
                first_act = False
            else:
                sol = sol + ", " + act
                
        solution_s1 = sol
        return confidence,solution_s1
    
    def calculate_correctness(self, problem, solution):
        if solution == "noSolution":
            return 0

        stringSolution = ""
        count = 1

        for elem in solution:
            stringSolution += elem
            if count < len(solution):
                stringSolution += ", "
                count +=1

        #print(f"String solution: {stringSolution}")

        #print("Execution Line is:  sh ./Planners/EFP/scripts/validate_solution.sh " + instanceNameEFP + " " + stringSolution)
        #Classical
        #print(f"Domain file is {domainFile}")
        
        ######################@TODO: DEBUG ROCKET SPECIFIC INSIDE THE FUNCTION
        domain,problem=utilities.split_names(problem_id)

        
        return SubgoalCompleteness.get_correctness(domain,stringSolution,problem)

class CustomSystem2Solver(sofai.System2Solver):
    def solve(self, problem):
        domain,problem=utilities.split_names(problem_id)
        
        head_tail = os.path.split(domain)
        domainFileNoPath = head_tail[1]
        domainPath = head_tail[0] + "/"

        head_tail = os.path.split(problem)
        problemFileNoPath = head_tail[1]
        problemPath = head_tail[0] + "/"

        result = subprocess.run(['bash','./'+ scripts_folder + 'FASTDOWNWARD_solve.sh', domainFileNoPath, domainPath, problemFileNoPath, problemPath, " " + str(int(timeLimit))+"s"])
        resFilename = os.path.splitext(domainFileNoPath)[0]+os.path.splitext(problemFileNoPath)[0]+".out"
        solutionS2 = utilities.readSolutionFromFile("tmp/FastDownward/" + resFilename,0)
        time = utilities.readTimeFromFile("tmp/FastDownward/" + resFilename)
    
# Defining main function
def plan_solve(problem_id):
    # Instantiate solvers
    system1_solver = CustomSystem1Solver()
    system2_solver = CustomSystem2Solver()
    
    context_file=""
    thresholds_file=""

    # Use metacognition to decide final solution
    final_solution = sofai.metacognition(problem_id, system1_solver, system2_solver,context_file, thresholds_file)
    print("Final Solution:", final_solution)

if __name__=="__main__":
    problem_name = "problem_01.pddl"
    domain_name = "domain_01.pddl"
    problem_id = utilities.unify_names(problem_name,domain_name)
    plan_solve(problem_id)