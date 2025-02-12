from ast import unaryop
import random
import sys
import json
import os
#from turtle import right

# Get the directory of the current script, i.e., 'AI Planning/problem generators/blocksworld'
script_directory = os.path.dirname(os.path.abspath(__file__))

# Go one level up to get to 'AI Planning/problem generators'
problem_generators_path = os.path.dirname(script_directory)

# Insert the 'problem generators' directory to sys.path
sys.path.insert(1, problem_generators_path)

import plansformer_prompt_generator as prompt_generator
import count_512subset as tokenizer

def write_to_pddl( problem_name, objects, init_state, goal_state ):
    print(problem_name)
    with open('problem_template.pddl', 'r') as f:
        lines = f.readlines()
        for l in range(len(lines)):
            if '(problem' in lines[l]:
                problem_line = l
            if '(:objects' in lines[l]:
                objects_line = l


    lines[problem_line] = '(define (problem '+problem_name+')\n'
    lines[objects_line] = '(:objects \n'+objects+' )\n'
    
    for i in range(len(lines)):
        if '(:init' in lines[i]:
            initial_line = i+1
    lines[initial_line] = init_state
    
    for i in range(len(lines)):
        if '(:goal' in lines[i]:
            goal_line = i+1
    lines[goal_line] = goal_state

    if os.path.exists('problems/') == False:
        os.mkdir('problems/')

    with open('problems/'+problem_name+'.pddl', 'w') as write_file:
        lines = "".join(lines)
        write_file.write(lines)
    write_file.close()


def generate_init_goal_states(init, goal, robots_list, balls, robots, rooms):
    
    init_list_balls = [int(i) for i in init.split('\n')[0].split(' ')]
    goal_list_balls = [int(i) for i in goal.split('\n')[0].split(' ')]
    
    robots_list_str = ['robot'+str(i+1) for i in range(robots)]
    left_gripper_list = ['lgripper'+str(i+1) for i in range(robots)]
    right_gripper_list = ['rgripper'+str(i+1) for i in range(robots)]
    
    rooms_list = ['room'+str(i+1) for i in range(rooms)]
    balls_list = ['ball'+str(i+1) for i in range(balls)]
    
    objects_list = ' '.join(robots_list_str) + ' - robot' + '\n' + ' '.join(left_gripper_list + right_gripper_list) + ' - gripper' + '\n' + ' '.join(rooms_list) + ' - room' + '\n' + ' '.join(balls_list) + ' - object'
    
    init_items = []
    
    for i in range(len(robots_list)):
        init_items.append( f'(at-robby robot{i+1} room{robots_list[i]})' )
        init_items.append( f'(free robot{i+1} lgripper{i+1})' )
        init_items.append( f'(free robot{i+1} rgripper{i+1})' )
    
    for i in range(len(init_list_balls)):
        init_items.append( f'(at ball{i+1} room{init_list_balls[i]})' )
    
    
    goal_items = []
    for i in range(len(goal_list_balls)):
        goal_items.append( f'(at ball{i+1} room{goal_list_balls[i]})' )
    
    
    return objects_list, '\n'.join(init_items), '\n'.join(goal_items)


def generate_state_combinations( list_of_states, balls, robots, rooms, number_of_files ):
    print(f'Generating Problem Files for {balls} balls, {robots} robots, {rooms} rooms ', end = ' ')
    name = f'problem_{balls}_{robots}_{rooms}_'
    counter = 0

    # for i in list_of_states:
    #     for j in list_of_states:
    #         if i != j:
    #             robots_list = [random.choice(rooms_list) for i in range(robots)]
    #             counter += 1
    #             objects, init_string, goal_string = generate_init_goal_states(i,j, robots_list, balls, robots, rooms)
    #             write_to_pddl(name+str(counter), objects, init_string, goal_string)

    while len(list_of_states) > 0:
        
        i = random.choice(list_of_states)
        list_of_states.remove(i)
        
        if len(list_of_states) == 0:
            break
        
        j = random.choice(list_of_states)
        list_of_states.remove(j)
        
        robots_list = [random.choice(rooms_list) for i in range(robots)]
        counter += 1
        objects, init_string, goal_string = generate_init_goal_states(i,j, robots_list, balls, robots, rooms)
        write_to_pddl(name+str(counter), objects, init_string, goal_string)
        
        prompt_string = prompt_generator.get_prompt('domain.pddl', 'problems/'+name+str(counter)+'.pddl')
        number_of_tokens = tokenizer.count_tokens(prompt_string)
        
        if number_of_tokens > 512:
            os.remove('problems/'+name+str(counter)+'.pddl')
            counter -= 1
            continue
        print(number_of_tokens, end = " ")
                
        if counter >= number_of_files:
            break

    print('problem file count = ', counter)

if __name__ == "__main__":

    number_of_robots = int(sys.argv[1])
    number_of_rooms = int(sys.argv[2])
    number_of_balls = int(sys.argv[3])    
    number_of_files = int(sys.argv[4])
    
    rooms_list = [i for i in range(1,number_of_rooms+1)]
    
    balls_list = [0 for i in range(number_of_balls)]
    
    states_dict = {}
    states_dict[number_of_balls] = []
    unique_states = set(list())
    for i in range(10000):
        for i in range(number_of_balls):
            balls_list[i] = random.choice(rooms_list)
            
        str_state = ' '.join(str(i) for i in balls_list)
        
        if str_state not in unique_states:
            unique_states.add(str_state)
            states_dict[number_of_balls].append(str_state)
    
    # print(len(states_dict[number_of_balls]))
    # print(states_dict[number_of_balls][0])
    
    # generate_init_goal_states( states_dict[number_of_balls][0], states_dict[number_of_balls][1], number_of_balls, number_of_robots, number_of_rooms)

    generate_state_combinations( states_dict[number_of_balls], number_of_balls, number_of_robots, number_of_rooms, number_of_files )