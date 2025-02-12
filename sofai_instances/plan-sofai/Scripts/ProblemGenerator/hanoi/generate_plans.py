import os
import sys
import glob
import pandas as pd
import time

domain_name = 'hanoi'

def execute_planner( current_path, planner_path, plan, domain, problem  ):
    
	os.chdir(planner_path)
	print(os.getcwd())
	command_str = f'./fast-downward.py --plan-file {plan} {domain} {problem} --search "astar(lmcut(verbosity=normal, transform=no_transform(), cache_estimates=true))"'
	os.system(command_str)
	print("Generated ",plan.split('/')[-1])
	os.chdir(current_path)

current_path = os.getcwd()
planner_path = current_path + '/fast-downward'

current_path = os.getcwd()

domain_folder = current_path + '/Domains/' + domain_name
domain_file = domain_folder + '/domain.pddl'

problems_path = domain_folder + '/problems/'
problem_files = glob.glob(problems_path + '*.pddl')

if os.path.exists(domain_folder):
	print('Problems folder exists')

# sort problem files by name
problem_files.sort()


print(domain_file, problems_path, planner_path)
print(problem_files[0])
for prob in problem_files:

	file_name = prob.split('/')[-1].replace('.pddl','.txt').replace('prob','plan_')

	if os.path.exists(domain_folder + '/plans/') == False:
		os.mkdir(domain_folder + '/plans/')

	plan_file = domain_folder + '/plans/' + file_name

	print(file_name)

	if os.path.exists(plan_file) == True:
		continue
	
	execute_planner( current_path, planner_path, plan_file, domain_file, prob)