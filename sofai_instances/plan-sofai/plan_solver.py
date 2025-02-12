import os
import subprocess
import traceback
import logging
import time

from Planners.New_PlansformerS1 import mode0 as newPlansformer_s1

from Planners.PDDL_parser import classical_parser
from Planners.PDDL_parser import SubgoalCompleteness

import utilities_plan
scripts_folder = "Scripts/"

#import sofai_tool as sofai
from sofai_tool.solvers import system1 as sofai1
from sofai_tool.solvers import system2 as sofai2
from sofai_tool.metacognition import metacognition_module as meta



class CustomSystem1Solver(sofai1.System1Solver):
    def solve(self, problem_id):
        
        problem,domain=utilities_plan.split_names(problem_id)
        
        timerSolving = time.time()
        try:
            tens_confidence, plan = newPlansformer_s1.solve(domain,problem,0)
        except Exception as e:
            logging.error(traceback.format_exc())
            raise Exception("System-1 encountered some errors.")

        confidence = float(utilities_plan.tensor_clean(tens_confidence))
        
        self.running_time = time.time() - timerSolving

        sol = ""
        first_act = True
        for act in plan:
            if first_act:
                sol = act
                first_act = False
            else:
                sol = sol + ", " + act
                
        self.solution = sol
        self.confidence = confidence

    
    def calculate_correctness(self, problem):
        if self.solution == "noSolution":
            return 0

        stringSolution = ""
        count = 1

        for elem in self.solution:
            stringSolution += elem
            if count < len(self.solution):
                stringSolution += ", "
                count +=1
        
        problem,domain=utilities_plan.split_names(problem_id)

        self.correctness = SubgoalCompleteness.get_correctness(domain,problem)

class CustomSystem2Solver(sofai2.System2Solver):
    def solve(self, problem_id, time_limit):
        problem,domain=utilities_plan.split_names(problem_id)
                
        head_tail = os.path.split(domain)
        domainFileNoPath = head_tail[1]
        domainPath = head_tail[0] + "/"

        head_tail = os.path.split(problem)
        problemFileNoPath = head_tail[1]
        problemPath = head_tail[0] + "/"

        timerSolving = time.time()

        result = subprocess.run(['bash','./'+ scripts_folder + 'FASTDOWNWARD_solve.sh', domainFileNoPath, domainPath, problemFileNoPath, problemPath, " " + str(int(time_limit))+"s"])
        resFilename = os.path.splitext(domainFileNoPath)[0]+os.path.splitext(problemFileNoPath)[0]+".out"
        solutionS2 = utilities_plan.readSolutionFromFile("tmp/FastDownward/" + resFilename,0)
        #time = utilities_plan.readTimeFromFile("tmp/FastDownward/" + resFilename)
        
        self.running_time = time.time() - timerSolving

        
        self.confidence = 1.0
        self.solution = solutionS2
    
    def estimate_difficulty(self,problem_id):
        problem,domain=utilities_plan.split_names(problem_id)
        
        domain_name, problem_name, init_States, goal_States, number_of_actions, number_of_predicates = classical_parser.get_details(domain,problem)
        
        #For now difficulty evaluation that does not consider goal or initial state (Maybe include planning graph lenght?)

        #domain_name, problem_name, init_States, goal_States, number_of_actions, number_of_predicates = classical_parser.get_details(domainFile,problemFile)
        intersection = [value for value in goal_States if value in init_States]
        diff_fluents = len(goal_States) - len(intersection)

        #print("Difficulty is: " + str(diff_fluents*number_of_actions*pow(2, number_of_predicates)))
        #sys.exit(0)

        return (diff_fluents*number_of_actions*pow(2, number_of_predicates))

    def calculate_correctness(self, problem):
        self.correctness = 1.0

    
# Defining main function
def plan_solve(problem_id):
    # Instantiate solvers
    system1_solver = CustomSystem1Solver()
    system2_solver = CustomSystem2Solver()
    
    context_file="context.txt"
    thresholds_file="thresholds.txt"
    experience_file = "plan_experience.json"
    new_run = False
    run_type = "sofai" # Possible values: "s1" "s2" "sofai"
    
    meta.metacognition(problem_id, system1_solver, system2_solver, context_file, thresholds_file, experience_file, new_run, run_type)
    

if __name__=="__main__":
    problem_name = "/mnt/c/Users/fraano/Desktop/Repos/sofai_tool/sofai_instances/plan-sofai/problem.pddl"
    domain_name = "/mnt/c/Users/fraano/Desktop/Repos/sofai_tool/sofai_instances/plan-sofai/domain.pddl"
    
    problem_id = utilities_plan.unify_names(problem_name,domain_name)
    
    plan_solve(problem_id)