# metacognition/metacognition_module.py

def try_s1(problem,s1_solution)
    s1_correctness = system1_solver.get_correctness(problem,s1_solution)
    if (s1_correctness >= correctnessCntx):
        model_of_self.memorize_solution(systemONE, plannerS1, s1_confidence, timerS1, s1_correctness, solutionS1, timerComputation)
        print(f"Solution found by System 1: {s1_solution} with correctness {s1_correctness}")
        exit(0)
    return s1_correctness

def metacognition(s1_solution, s1_confidence, problem, system2_solver, confidence_threshold=1):
    # system2_solver = system2_solver
    # confidence_threshold = confidence_threshold
    # s1_solution = s1_solution
    # confidence = confidence
    # problem = problem
    # if confidence >= confidence_threshold:
    #     return s1_solution  # Return System 1 solution if confidence is sufficient
    # else:
    #     return system2_solver.solve(problem)  # Call System 2 otherwise


    ''' SYSTEM-1 METACOGNITIVE MODULE'''
    
    ### First Metacognition process
    ## We first check if System-2 has generated at least an experience of n > threshold1 entries to allow System-1 to continue
    M = 1
    tested_s1 = False
    correctness_s1=0
    if (model_of_self.count_solved_instances(systemALL,plannerALL) > threshold1):
        ## We then check if System-1 has generated at least m > threshold4 plans to evaluate its performance and check if it make sense to verify it
        if (model_of_self.count_solved_instances(systemONE,plannerALL) > threshold4):
            M = 1-model_of_self.get_avg_corr(systemONE,plannerALL,threshold4)
        else:
            M = 0

        if (s1_confidence * (1-M) > confidence_threshold):
            try_s1(problem,s1_solution)
            #Exiting from function already implied that S1 is not good enough
            return system2_solver.solve(problem)
            tested_s1 = True #Never reached


    ''' SYSTEM-2 METACOGNITIVE MODULE'''
    
    estimated_time_s2 = system2_solver.estimate_time_consumption(problem)
    estimated_cost_s2 = sys.maxsize

    ## We check if the estimated time is enough to solve the problem
    reamining_time = time_limit - (time.time() - encompassed_time)
    if(reamining_time - estimated_time_s2 > 0):
        estimated_cost_s2 = estimated_time_s2 / remainingTime

    ## If we think that there is not enough time to employ System-2, we check System-1 solution even if it has low confidence value
    if (estimated_cost_s2 > 1 and (not tested_s1)):
        try_s1(problem,s1_solution)
        #Exiting from function already implied that S1 is not good enough
        return system2_solver.solve(problem)
        tested_s1 = True #Never reached


    ### Trying to employ System-2
    ## If System-1 had low confidence (or failed) we try to employ System-2
    # if System-1 failed we try using System-2 even if we think that we do not have ebough time
    else:
        ## This first block of code randomly (with probability of epsilon) employs System-1 to give it more chance 
        probability_s1 = (1-threshold3)*epsilon_s1
        if (probability_s1 > random.random() and (not tested_s1)):
            try_s1(problem,s1_solution)
            #Exiting from function already implied that S1 is not good enough
            return system2_solver.solve(problem)
            tested_s1 = True #Never reached
        
        ## Instead, with 1-epsilon, we use the ''standard'' metacognitive path
        else:
            if (len(solutionS1) > 0):
                ## Instead, with 1-epsilon, we use the ''standard'' metacognitive path
                # @TODO Here we calcuate the correctness once again, check the part where we refrain to calculate it
                if(not tested_s1):
                    s1_correctness = system1_solver.get_correctness(problem,s1_solution)

                ## Here we check if we can improve on the System-1 results
                if (s1_correctness >= correctnessCntx):
                    if((1-(estimated_cost_s2 * (1-threshold3))) > (s1_correctness*(1-M))):
                        if (not system2_solver.solve(problem))#(remainingTime,plannerS2,solutionS1,s1_correctness,timerComputation)):
                            model_of_self.memorize_solution(systemONE, plannerS1, confidenceS1, timerS1, s1_correctness, solutionS1, timerComputation)
                    else:
                        model_of_self.memorize_solution(systemONE, plannerS1, confidenceS1, timerS1, s1_correctness, solutionS1, timerComputation)

    ### Finally we run System-2 only if the available time is within reasonable distance w.r.t. the time we think that the System-2 is goin to take 
    ## We arbitrary set the extra time to be 50%
    flexibility_perc = 50
    if (remainingTime >= (estimated_time_s2 - (float(estimated_time_s2)/100.0 * float(flexibility_perc)))):
        system2_solver.solve(problem)#(remainingTime,plannerS2,solutionS1,s1_correctness,timerComputation)

    model_of_self.end_computation 