### Thresholds
threshold1 = 20     #This threshold represents the minimun number of plan (existence) that needs to be generated from System-2 (in the same domain) before accepting System-1 solution
threshold2 = 0.8    #The value which current_reward/average_revard must surpass to eploy System-1 -- FOR NOW NOT USED
threshold3 = 0.9    #This value represents the risk-adversion of the system -- The higher it is the more incline to use System-2 the system is
threshold4 = 20     #This is the threshold that is used to set 'M' = 1 when System-1 hasn't enough experience,
epsilonS1 = 0.1
correctness_threshold = 1.0

time_limit=60

maxExperience = 1000