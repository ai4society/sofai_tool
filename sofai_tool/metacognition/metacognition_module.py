from . import utilities
from . import mos as model_of_self
import sys
import random
import time
import pdb

### Type of Systems
systemALL = -1              # Constant that represents both System-1 and System-2
systemONE = 1               # Constant that represents only System-1
systemTWO = 2               # Constant that represents only System-2

### Type of Planners
plannerALL = -1             # Constant that represents all the possible Planners (both in System-1 and System-2)
confidenceS1 = 0
# difficulty = 0

tested_s1 = False
tested_s2 = False

def try_s1(problemId,system1_solver,correctness_threshold,timerSOFAI, run_type):
    global tested_s1
    if not tested_s1:
        tested_s1 = True
        system1_solver.calculate_correctness(problemId)
        if (system1_solver.correctness >= correctness_threshold):
            if run_type=='sofai':
              model_of_self.memorize_solution(system1_solver,systemALL, problemId, timerSOFAI, 0)
            #print(f"Solution found by System 1: {system1_solver.solution} with correctness {system1_solver.correctness}")
            else:
              model_of_self.memorize_solution(system1_solver,systemONE, problemId, timerSOFAI, 0)
            return True
        return False
    else:
        return False

def try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context,difficulty, run_type):
    global tested_s2
    if not tested_s2:
        tested_s2 = True
        
        if difficulty < 0:
            difficulty = system2_solver.estimate_difficulty(problemId)
        
        system2_solver.solve(problemId,time_limit_context - (time.time() - timerSOFAI))
        system2_solver.calculate_correctness(problemId)
        if (system2_solver.correctness >= correctness_threshold):
            if run_type=='sofai':
              model_of_self.memorize_solution(system2_solver,systemALL, problemId, timerSOFAI, difficulty)
            else:
              model_of_self.memorize_solution(system2_solver,systemTWO, problemId, timerSOFAI, difficulty)
            return True
        return False
    else:
        return False


def metacognition(problemId, system1_solver, system2_solver, context_file, thresholds_file, experience_file, new_run, run_type):
    global tested_s2
    global tested_s1
    tested_s1 = False
    tested_s2 = False

    model_of_self.createFolders(experience_file, new_run)
    
    #Parse context and thresholds information
    T1,T2,T3,T4,epsilon_s1=utilities.read_threshold(thresholds_file)
    time_limit_context = float(utilities.get_var_from_file(context_file,"time_limit"))
    correctness_threshold = float(utilities.get_var_from_file(context_file,"correctness_threshold"))
    
    ### Special cases for testing
    if run_type == "s1":
        timerSOFAI = time.time()
        system1_solver.solve(problemId)
        if not try_s1(problemId,system1_solver,correctness_threshold,timerSOFAI,run_type):
            utilities.end_computation(problemId, timerSOFAI)
        return
    if run_type == "s2":
        timerSOFAI = time.time()
        if not try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context, -1, run_type):
            utilities.end_computation(problemId, timerSOFAI)
        return
    

    ''' SYSTEM-1 METACOGNITIVE MODULE'''
    # Solve with System 1 and estimate confidence
    timerSOFAI = time.time()
    system1_solver.solve(problemId) #This stores solution and confidence in S1
    ### First Metacognition process
    ## We first check if System-2 has generated at least an experience of n > threshold1 entries to allow System-1 to continue
    M = 1 # represents average correct value

    ## We first check if SOFAI has generated at least an experience of n > threshold1 entries to allow System-1 to continue
    if (model_of_self.count_solved_instances(systemALL) > T1):
        ## We check if System-1 has generated at least m > threshold4 plans to evaluate its performance and check if it make sense to verify it
        if (model_of_self.count_solved_instances(systemONE) > T4):
            M = 1-model_of_self.get_avg_corr(systemONE,T4)
        else:
            M = 0
        if (system1_solver.confidence * (1-M) >= T3):
            # print("---------------HERE 1")
            if not try_s1(problemId,system1_solver,correctness_threshold,timerSOFAI,run_type):
                if not try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context,-1, run_type):
                    utilities.end_computation(problemId, timerSOFAI)
            return

    ''' SYSTEM-2 METACOGNITIVE MODULE'''
    estimated_difficulty_s2 = system2_solver.estimate_difficulty(problemId)
    estimated_time_s2 = model_of_self.estimate_time_consumption(problemId, estimated_difficulty_s2)
    estimated_cost_s2 = sys.maxsize 

    ## We check if the estimated time is enough to solve the problem
    remaining_time = time_limit_context - (time.time() - timerSOFAI)
    if(remaining_time - estimated_time_s2 > 0):
        estimated_cost_s2 = estimated_time_s2 / remaining_time

    ## If we think that there is not enough time to employ System-2, we check System-1 solution even if it has low confidence value
    if (estimated_cost_s2 > 1):
        # print("---------------HERE 2")
        if not try_s1(problemId,system1_solver,correctness_threshold,timerSOFAI,run_type):
            if not try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context,estimated_difficulty_s2,run_type):
                utilities.end_computation(problemId, timerSOFAI)
        return

    ### Trying to employ System-2
    ## If System-1 had low confidence (or failed) we try to employ System-2
    # if System-1 failed we try using System-2 even if we think that we do not have ebough time
    else:
        ## This first block of code randomly (with probability of epsilon) employs System-1 to give it more chance 
        probability_s1 = (1-T3)*epsilon_s1
        r_value = random.random()
        if (probability_s1 > r_value):
            # print("---------------HERE 3")
            if not try_s1(problemId,system1_solver,correctness_threshold,timerSOFAI,run_type):
                if not try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context,estimated_difficulty_s2,run_type):
                    utilities.end_computation(problemId, timerSOFAI)
            return
        
        ## Instead, with 1-epsilon, we use the ''standard'' metacognitive path
        else:
            if(not tested_s1):
                system1_solver.calculate_correctness(problemId)
                ## Here we check if we can improve on the System-1 results
            if (system1_solver.correctness >= correctness_threshold):
                # print("---------------HERE 4")
                if((1-(estimated_cost_s2 * (1-T3))) > (system1_solver.correctness*(1-M))):
                    if try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context,estimated_difficulty_s2,run_type):
                        return
     
                #If we exit from try_s2 then no solution is found
                model_of_self.memorize_solution(system1_solver,systemALL, problemId, timerSOFAI, estimated_difficulty_s2)
                return
    ### Finally we run System-2 only if the available time is within reasonable distance w.r.t. the time we think that the System-2 is goin to take 
    ## We arbitrary set the extra time to be 50%
    flexibility_perc = 50
    if ((time.time() - timerSOFAI) >= (estimated_time_s2 - (float(estimated_time_s2)/100.0 * float(flexibility_perc)))):
        # print("---------------HERE 5")
        if try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context,estimated_difficulty_s2,run_type):
            return

    utilities.end_computation(problemId, timerSOFAI) # it is going to this one at the end, means it is not going inside any if loop above!, not directly, none of the if loop conditions are getting true!
