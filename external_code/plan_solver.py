import os
import subprocess
import traceback
import logging


from Planners.New_PlansformerS1 import mode0 as newPlansformer_s1

from Planners.PDDL_parser import classical_parser
from Planners.PDDL_parser import SubgoalCompleteness

import utilities
scripts_folder = "Scripts/"

#import sofai_tool as sofai
from sofai_tool.solvers import system1 as sofai1
from sofai_tool.solvers import system2 as sofai2


class CustomSystem1Solver(sofai1.System1Solver):
    def solve(self, problem_id):
        
        problem,domain=utilities.split_names(problem_id)
        
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
        
        problem,domain=utilities.split_names(problem_id)

        ######################@TODO: DEBUG ROCKET SPECIFIC INSIDE THE FUNCTION        
        return SubgoalCompleteness.get_correctness(domain,solution,problem)

class CustomSystem2Solver(sofai2.System2Solver):
    def solve(self, problem, time_limit):
        problem,domain=utilities.split_names(problem_id)
        
        print(f"Domain {domain} and problem {problem}")
        
        head_tail = os.path.split(domain)
        domainFileNoPath = head_tail[1]
        domainPath = head_tail[0] + "/"

        head_tail = os.path.split(problem)
        problemFileNoPath = head_tail[1]
        problemPath = head_tail[0] + "/"

        result = subprocess.run(['bash','./'+ scripts_folder + 'FASTDOWNWARD_solve.sh', domainFileNoPath, domainPath, problemFileNoPath, problemPath, " " + str(int(time_limit))+"s"])
        print(f"Result is {result}")
        resFilename = os.path.splitext(domainFileNoPath)[0]+os.path.splitext(problemFileNoPath)[0]+".out"
        solutionS2 = utilities.readSolutionFromFile("tmp/FastDownward/" + resFilename,0)
        time = utilities.readTimeFromFile("tmp/FastDownward/" + resFilename)
        
        print(f"Problem {problem} has been solved by FD in {time} with solution {solutionS2}")
        return solutionS2
    
    def estimateDifficulty(problem,domain):
        
        domain_name, problem_name, init_States, goal_States, number_of_actions, number_of_predicates = classical_parser.get_details(domain,problem)
        
        #For now difficulty evaluation that does not consider goal or initial state (Maybe include planning graph lenght?)

        #domain_name, problem_name, init_States, goal_States, number_of_actions, number_of_predicates = classical_parser.get_details(domainFile,problemFile)
        intersection = [value for value in goal_States if value in init_States]
        diff_fluents = len(goal_States) - len(intersection)

        #print("Difficulty is: " + str(diff_fluents*number_of_actions*pow(2, number_of_predicates)))
        #sys.exit(0)

        return (diff_fluents*number_of_actions*pow(2, number_of_predicates))

    
# Defining main function
def plan_solve(problem_id):
    # Instantiate solvers
    system1_solver = CustomSystem1Solver()
    system2_solver = CustomSystem2Solver()
    
    context_file=""
    thresholds_file=""

    # Use metacognition to decide final solution
    #final_solution = sofai.metacognition(problem_id, system1_solver, system2_solver,context_file, thresholds_file)
    #print("Final Solution:", final_solution)

    confidence,sol=system1_solver.solve(problem_id)
    #sol=system2_solver.solve(problem_id)
    correctness=system1_solver.calculate_correctness(problem_id,sol)
    print(f"Problem {problem_id} has been solved with conf {confidence} and corr {correctness} with solution {sol}")


if __name__=="__main__":
    #COmment on solution format fir validator
    problem_name = "/mnt/c/Users/franc/Desktop/Repos/SOFAI_tutorial/problem.pddl"
    domain_name = "/mnt/c/Users/franc/Desktop/Repos/SOFAI_tutorial/domain.pddl"
    problem_id = utilities.unify_names(problem_name,domain_name)
    plan_solve(problem_id)