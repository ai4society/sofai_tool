import random
import sys
import os


def print_to_pddl( problem_name, objects, init_state, goal_state ):
    with open('hanoi/problem_template.pddl', 'r') as f:
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

    lines = "".join(lines)
    print(lines)

def write_to_pddl( problem_name, objects, init_state, goal_state, block_number ):
    print(problem_name)
    with open('problem_template.pddl', 'r') as f:
        lines = f.readlines()
        for l in range(len(lines)):
            if '(problem' in lines[l]:
                problem_line = l
            if '(:objects' in lines[l]:
                objects_line = l
            if '(:init' in lines[l]:
                initial_line = l+1

    lines[problem_line] = '(define (problem '+problem_name+')\n'
    lines[objects_line] = '(:objects '+objects+')\n'
    lines.insert( initial_line, init_state )
    for l in range(len(lines)):
        if '(:goal' in lines[l]:
            goal_line = l+2
    lines.insert( goal_line, goal_state)

    if os.path.exists('problems/') == False:
        os.mkdir('problems/')

    with open('problems/'+problem_name+'.pddl', 'w') as write_file:
        lines = "".join(lines)
        write_file.write(lines)
    write_file.close()


def check_valid(array,number):

    if number == -1 or number == -2 or number == -3:
        return True

    item = (len(array) + 1)
    check_set = set([item])

    flag = 1
    return_val = True
    while( flag ):
        item = (number-1)
        if item < len(array) and item >= 0:
            number = array[item]

            if number == -1 and number == -2 and number == -3:
                return True

            if number in check_set:
                flag = 0
                return_val = False
        else:
            flag = 0

    return return_val


def generate_states(number_of_blocks, pegs_blocks_list):

    state_array = [0 for i in range(number_of_blocks)]
    
    block_Set = set(list([]))
    peg_list = [-1,-2,-3]
    for i in range(len(state_array)-1, -1, -1):
        
        target_block_list = list(range(i+2,number_of_blocks+1))
        item_choice = random.choice( peg_list + target_block_list )
        # print(block_Set, item_choice)
        
        if item_choice in peg_list:
            # remove item from peg_list
            peg_list.remove(item_choice)
        
        while item_choice in block_Set:
            item_choice = random.choice( peg_list + target_block_list )
        
        block_Set.add(item_choice)

        state_array[i] = item_choice
    # print(state_array, target_block_list, block_Set)
    # peg_temp_array = pegs_blocks_list
    # state_array = []
    # block_set = set(list())
    # for i in range( number_of_blocks ):

    #     flag = True
    #     while( flag ):

    #         number = random.choice(peg_temp_array)
            
    #         # print(number, state_array, peg_temp_array)
            
    #         if number not in block_set and number != (i+1):
    #             temp_array = state_array
                
    #             valid_case = check_valid(temp_array,number)

    #             if valid_case:
    #                 state_array.append(number)
    #                 if number == -1 or number == -2 or number == -3:
    #                     peg_temp_array.remove(number)
    #                 else:
    #                     block_set.add(number)
    #                 flag = False

    return state_array


def generate_init_goal_states( init, goal):
    init = [int(item) for item in init.split(' ')]
    goal = [int(item) for item in goal.split(' ')]

    max_blocks = max( len(init), len(goal) )

    pegs = ['peg1','peg2','peg3']
    objects = ['peg1','peg2','peg3']
    for blocks in range(1,max_blocks+1):
        objects.append( 'd'+str(blocks) )

    init_items = []
    
    for peg in pegs:
        for obj in objects:
            if 'peg' not in obj:
                init_items.append(f'(smaller {peg} {obj})')
            
    for obj in range(3,len(objects)):
        for obj2 in range(obj+1,len(objects)):
            init_items.append(f'(smaller {objects[obj2]} {objects[obj]})')
            
    for item in range(len(init)):
        if init[item] == -1:
            init_items.append(f'(on {objects[item+3]} {objects[0]} )')
        elif init[item] == -2:
            init_items.append(f'(on {objects[item+3]} {objects[1]} )')
        elif init[item] == -3:
            init_items.append(f'(on {objects[item+3]} {objects[2]} )')
        else:
            init_items.append('(on '+objects[item+3]+' '+objects[init[item]-1+3]+')')
            
        if (item+1) not in init:
            init_items.append('(clear '+objects[item+3]+')')
        
    if -1 not in init:
        init_items.append('(clear '+objects[0]+')')
    if -2 not in init:
        init_items.append('(clear '+objects[1]+')')
    if -3 not in init:
        init_items.append('(clear '+objects[2]+')')

    goal_items = []
    for item in range(len(goal)):
        if goal[item] == -1:
            goal_items.append(f'(on {objects[item+3]} {objects[0]} )')
        elif goal[item] == -2:
            goal_items.append(f'(on {objects[item+3]} {objects[1]} )')
        elif goal[item] == -3:
            goal_items.append(f'(on {objects[item+3]} {objects[2]} )')
        else:
            goal_items.append('(on '+objects[item+3]+' '+objects[goal[item]-1+3]+')')
        if (item+1) not in goal:
            goal_items.append('(clear '+objects[item+3]+')')
            
    if -1 not in goal:
        goal_items.append('(clear '+objects[0]+')')
    if -2 not in goal:
        goal_items.append('(clear '+objects[1]+')')
    if -3 not in goal:
        goal_items.append('(clear '+objects[2]+')')

    return ' '.join(objects), '\n'.join(init_items), '\n'.join(goal_items)


def generate_single_state_( list_of_states,block_number, number_of_files ):
    name = 'problem_'+str(block)+'_'
    
    dir_path = 'hanoi/problem_files_temp'
    os.makedirs(dir_path, exist_ok=True) 

    name += str(len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))]))

    temp_dic = {}

    if len(list_of_states) > 0:
        pick_one = random.choice(list_of_states)
        pick_two = random.choice(list_of_states)
        if pick_one != pick_two:
            if pick_one + pick_two not in temp_dic:
                temp_dic[pick_one + pick_two] = True
                objects, init_string, goal_string = generate_init_goal_states(pick_one,pick_two)
                print_to_pddl(name, objects, init_string, goal_string)



if __name__ == "__main__":
    blocks = int(sys.argv[1])
    blocks_list = [i for i in range(1,blocks)]
    pegs_list = [-1,-2,-3]

    pegs_blocks_list = pegs_list.extend(blocks_list)

    states_dict = {}
    block = random.randint(2, blocks+1)

    states_dict[block] = []
    unique_states = set(list())
        
    for i in range(10000):
        state = generate_states(block, pegs_blocks_list)
        str_state = " ".join(str(item) for item in state)
        if str_state not in unique_states:
            unique_states.add(str_state)
            states_dict[block].append(str_state)
    generate_single_state_( states_dict[block],block, 1 )