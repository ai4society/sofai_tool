import re


def find_parens(s):
    toret = {}
    pstack = []
    flag = 0
    for i, c in enumerate(s):
        #print("i is " + str(i) + " c is " + str(c))

        if flag == 1 and len(pstack) == 0:
            return toret

        if c == '(':
            pstack.append(i)
            flag = 1
        elif c == ')':
            toret[pstack.pop()] = i

    #print("To ret is: " +  str(toret))
    #print("To ret 0 is: " +  str(toret[0]))
    return toret

def get_problem_name(file):
    problem_name = ''
    domain_name = ''
    with open(file,'r') as f:
        f = f.readlines()
        for line in f:
            if '(problem' in line:
                ind = line.index('(problem')
                problem_name =  line[ind:-1].strip('(problem')[:-1]
            if '(problem'.upper() in line:
                ind = line.index('(problem'.upper())
                problem_name =  line[ind:-1].strip('(problem'.upper())[:-1]

        for line in f:
            if '(:domain' in line:
                ind = line.index('(:domain')
                domain_name =  line[ind:-1].strip('(:domain')[:-1]
            if '(:domain'.upper() in line:
                ind = line.index('(:domain'.upper())
                domain_name =  line[ind:-1].strip('(:domain'.upper())[:-1]

    return problem_name, domain_name

def get_objects(file):

    with open(file) as f:
        file_data = f.read()
        start_index = file_data.index('(:objects')
        closing_ind = find_parens( file_data[start_index:] )[0]

        file_data = file_data[start_index+10: start_index + closing_ind]

        # print(file_data)
        instances_list = [item for item in file_data.split(' ') if item]

        if instances_list.count('-')>0:
            objects =  True
        else:
            objects =  False

        instances = {}
        temp_list = []
        flag = 1
        for item in instances_list:

            if objects == True:
                if item == '-':
                    flag = 0
                    continue
                if flag:
                    if '\n' in item:
                        temp_list.append(item.replace('\n',''))
                    else:
                        temp_list.append(item)
                else:
                    flag = 1
                    if '\n' in item:
                        temp_item = item.replace('\n','')
                    else:
                        temp_item = item

                    if temp_item not in instances:
                        instances[temp_item] = []
                    instances[temp_item].extend(temp_list)
                    temp_list = []
                    flag = 1

            else:

                if flag:
                    instances = []
                    flag = 0

                if '\n' in item:
                    instances.append(item.replace('\n',''))
                else:
                    instances.append(item)


    return instances

def get_initialState(file):
    with open(file) as f:
        file_data = f.read()
        start_index = file_data.index('(:init')
        closing_idx = find_parens( file_data[start_index:] )[0]

        file_data = file_data[ start_index: start_index + closing_idx+1]

        index_dict = find_parens( file_data )
        ind_list = sorted(list(index_dict.keys()))[1:]


        if "and" in file_data[ind_list[0]:ind_list[0]+4]:
            ind_list = ind_list[1:]

        states = []
        previoud_ind = -1
        for ind in ind_list:
            if ind > previoud_ind:
                to_add = file_data[ ind: index_dict[ind]+1]
                to_add = to_add.replace("(","")
                to_add = to_add.replace(")","")
                states.append(to_add)
                previoud_ind = index_dict[ind]

        return states

def get_goalState(file):

    with open(file) as f:
        file_data = f.read()
        start_index = file_data.index('(:goal')
        closing_idx = find_parens( file_data[start_index:] )[0]



        file_data = file_data[ start_index : start_index + closing_idx + 1]
        #print("File data is: " + str(file_data))


        index_dict = find_parens( file_data )
        ind_list = sorted(list(index_dict.keys()))[1:]

        if "and" in file_data[ind_list[0]:ind_list[0]+4]:
            ind_list = ind_list[1:]

        states = []
        previoud_ind = -1
        for ind in ind_list:
            if ind > previoud_ind:
                to_add = file_data[ ind: index_dict[ind]+1]
                to_add = to_add.replace("(","")
                to_add = to_add.replace(")","")
                states.append(to_add)
                previoud_ind = index_dict[ind]


        return states
