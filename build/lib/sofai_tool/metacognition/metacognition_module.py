# metacognition/metacognition_module.py

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

def try_s1(problemId,system1_solver,s1_solution,correctness_threshold,s1_confidence,S1_time,timerSOFAI):
    global tested_s1
    if not tested_s1:
        tested_s1 = True
        s1_correctness = system1_solver.correctness
        if (s1_correctness >= correctness_threshold):
            model_of_self.memorize_solution(systemONE, problemId, s1_confidence, system1_solver.running_time, s1_correctness, s1_solution, timerSOFAI, 0)
            print(f"Solution found by System 1: {s1_solution} with correctness {s1_correctness}")
            sys.exit()
        return s1_correctness # no point returning any value!
    else:
        return -1

def try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context,difficulty=-1.0):
    global tested_s2
    if not tested_s2:
        tested_s2 = True
        
        if difficulty < 0:
            difficulty = system2_solver.estimate_difficulty(problemId)
        
        s2_confidence,s2_solution = system2_solver.solve(problemId,time_limit_context - (time.time() - timerSOFAI))
        s2_correctness = system2_solver.correctness
        if (s2_correctness >= correctness_threshold):
            model_of_self.memorize_solution(systemTWO,problemId, s2_confidence, system2_solver.running_time, s2_correctness, s2_solution, timerSOFAI, difficulty)
            print(f"Solution found by System 2: {s2_solution} with correctness {s2_correctness}")
            sys.exit()
        return s2_correctness # no point returning any value!
    else:
        return -1


def metacognition(problemId, system1_solver, system2_solver, context_file, thresholds_file, experience_file, new_run):
    global tested_s2
    global tested_s1
    tested_s1 = False
    tested_s2 = False

    model_of_self.createFolders(experience_file, new_run)
    
    #Parse context and thresholds information
    T1,T2,T3,T4,epsilon_s1=utilities.read_threshold(thresholds_file)
    time_limit_context = float(utilities.get_var_from_file(context_file,"time_limit"))
    correctness_threshold = float(utilities.get_var_from_file(context_file,"correctness_threshold"))
    
    #Start timing the solving process
    timerSOFAI = time.time()
    s1_correctness = 0
    s2_correctness = 0
    
    # Solve with System 1 and estimate confidence
    s1_confidence,s1_solution = system1_solver.solve(problemId)
    
    ''' SYSTEM-1 METACOGNITIVE MODULE'''
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
        if (s1_confidence * (1-M) >= correctness_threshold):
            s1_correctness = max(s1_correctness,try_s1(problemId,system1_solver,s1_solution,correctness_threshold,s1_confidence,system1_solver.running_time,timerSOFAI))
            s2_correctness = max(s2_correctness,try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context))
            utilities.end_computation(problemId, timerSOFAI)

    ''' SYSTEM-2 METACOGNITIVE MODULE'''
    estimated_difficulty_s2 = system2_solver.estimate_difficulty(problemId)
    estimated_time_s2 = model_of_self.estimate_time_consumption(problemId, estimated_difficulty_s2) #Look at function estimateTimeCons(planner,difficulty): of previous arch
    estimated_cost_s2 = sys.maxsize # check why is this here?

    ## We check if the estimated time is enough to solve the problem
    remaining_time = time_limit_context - (time.time() - timerSOFAI)
    if(remaining_time - estimated_time_s2 > 0):
        estimated_cost_s2 = estimated_time_s2 / remaining_time

    ## If we think that there is not enough time to employ System-2, we check System-1 solution even if it has low confidence value
    if (estimated_cost_s2 > 1):
        s1_correctness = max(s1_correctness,try_s1(problemId,system1_solver,s1_solution,correctness_threshold,s1_confidence,system1_solver.running_time,timerSOFAI)) #Exiting from function already implied that S1 is not good enough
        s2_correctness = max(s2_correctness,try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,estimated_difficulty_s2,time_limit_context))
        utilities.end_computation(problemId, timerSOFAI)

    ### Trying to employ System-2
    ## If System-1 had low confidence (or failed) we try to employ System-2
    # if System-1 failed we try using System-2 even if we think that we do not have ebough time
    else:
        ## This first block of code randomly (with probability of epsilon) employs System-1 to give it more chance 
        probability_s1 = (1-T3)*epsilon_s1
        r_value = random.random()
        if (probability_s1 > r_value):
            s1_correctness = max(s1_correctness,try_s1(problemId,system1_solver,s1_solution,correctness_threshold,s1_confidence,system1_solver.running_time,timerSOFAI)) #Exiting from function already implied that S1 is not good enough
            s2_correctness = max(s2_correctness,try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,estimated_difficulty_s2,time_limit_context))
            utilities.end_computation(problemId, timerSOFAI)
        
        ## Instead, with 1-epsilon, we use the ''standard'' metacognitive path
        else:
            if(not tested_s1):
                s1_correctness = system1_solver.correctness
                ## Here we check if we can improve on the System-1 results
            if (system1_solver.correctness >= correctness_threshold):
                if((1-(estimated_cost_s2 * (1-T3))) > (system1_solver.correctness*(1-M))):
                    try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,estimated_difficulty_s2) #If we exit from here, S2 could not find solution
                    model_of_self.memorize_solution(systemONE, problemId, confidenceS1, system1_solver.running_time, system1_solver.correctness, s1_solution, timerSOFAI,estimated_difficulty_s2)
                else:
                    model_of_self.memorize_solution(systemONE, problemId, confidenceS1, system1_solver.running_time, system1_solver.correctness, s1_solution, timerSOFAI,estimated_difficulty_s2)
                print(f"Solution found by System 1: {s1_solution} with correctness {system1_solver.correctness}")
                sys.exit()
    ### Finally we run System-2 only if the available time is within reasonable distance w.r.t. the time we think that the System-2 is goin to take 
    ## We arbitrary set the extra time to be 50%
    flexibility_perc = 50
    if ((time.time() - timerSOFAI) >= (estimated_time_s2 - (float(estimated_time_s2)/100.0 * float(flexibility_perc)))):
        try_s2(problemId,system2_solver,correctness_threshold,timerSOFAI,time_limit_context,estimated_difficulty_s2) #If we exit from here, S2 could not find solution

    utilities.end_computation(problemId, timerSOFAI) # it is going to this one at the end, means it is not going inside any if loop above!, not directly, none of the if loop conditions are getting true!