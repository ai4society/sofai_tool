import re


def find_parens(s):
    toret = {}
    pstack = []
    flag = 0
    for i, c in enumerate(s):

        if flag == 1 and len(pstack) == 0:
            return toret

        if c == '(':
            pstack.append(i)
            flag = 1
        elif c == ')':
            toret[pstack.pop()] = i

    return toret


def get_domain_name(file):
    with open(file,'r') as f:
        for line in f:
            if '(domain' in line:
                ind = line.index('(domain')
                return line[ind:-1].strip('(domain')[:-1]
            if '(domain'.upper() in line:
                ind = line.index('(domain'.upper())
                return line[ind:-1].strip('(domain'.upper())[:-1]

def get_requirements(file):

    with open(file) as f:
        file_data = f.read()
        requirement_index = file_data.index('(:requirements')
        present_text = file_data[requirement_index:requirement_index + find_parens(file_data[requirement_index:])[0]]

        return present_text.split()[1:]

def get_types(file):

    with open(file) as f:
        file_data = f.read()
        predicate_index = file_data.index('(:types')
        predicate_closing_ind = find_parens( file_data[predicate_index:] )[0]

        file_data = file_data[predicate_index+8: predicate_index + predicate_closing_ind]

        # print(file_data)
        types_list = [item for item in file_data.split(' ') if item]

        if types_list.count('-')>0:
            objects =  True 
        else:
            objects =  False

        types = {}
        temp_list = []
        flag = 1
        for item in types_list:

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

                    if temp_item not in types:
                        types[temp_item] = []
                    types[temp_item].extend(temp_list)
                    temp_list = []
                    flag = 1

            else:

                if flag:
                    types = []
                    flag = 0

                if '\n' in item:
                    types.append(item.replace('\n',''))
                else:
                    types.append(item)


    return types

def get_constants(file):

    with open(file) as f:
        file_data = f.read()
        predicate_index = file_data.index('(:constants')
        predicate_closing_ind = find_parens( file_data[predicate_index:] )[0]

        file_data = file_data[predicate_index+8: predicate_index + predicate_closing_ind]

        # print(file_data)
        constants_list = [item for item in file_data.split(' ') if item]

        if constants_list.count('-')>0:
            types =  True 
        else:
            types =  False

        constants = {}
        temp_list = []
        flag = 1
        for item in constants_list:

            if types == True:
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

                    if temp_item not in constants:
                        constants[temp_item] = []
                    constants[temp_item].extend(temp_list)
                    temp_list = []
                    flag = 1

            else:

                if flag:
                    constants = []
                    flag = 0

                if '\n' in item:
                    constants.append(item.replace('\n',''))
                else:
                    constants.append(item)

        return_dict = {}
        return_dict["constants"] = constants

    return return_dict["constants"]

def get_predicates(file):

    with open(file) as f:
        file_data = f.read()
        predicate_index = file_data.index('(:predicates')
        predicate_closing_ind = find_parens( file_data[predicate_index:] )[0]

        file_data = file_data[predicate_index: predicate_index + predicate_closing_ind+1]

        predicates_list = []
        for ind in range(1, len(file_data)):
            if file_data[ind] == "(":
                # print(ind,file_data[ind])
                closing_ind = find_parens( file_data[ind:] )[0]
                present_text = file_data[ ind : ind + closing_ind+1 ]
                predicates_list.append(present_text)

        return predicates_list

def get_params(data):

    params_index = data.index(':parameters')    
    index_dict = find_parens( data[params_index:] )
    data = data[params_index:]

    start_ind = list(index_dict.keys())[0]
    closing_ind = index_dict[start_ind]

    data_string = re.split(" +", data[start_ind+1:closing_ind].replace('-',''))

    values = []
    types = []
    flag = 1
    count = 1
    for i in data_string:
        if '?' in i:
            values.append(i)
            if flag == 0:
                count += 1
            flag = 0
        else:
            for c in range(count):
                types.append(i)
            flag = 1

    return_dict = dict()
    return_dict["parameters"] = {}
    return_dict["parameters"]["values"] = values
    return_dict["parameters"]["types"] = types

    return return_dict

def get_preconditions(data):

    index = data.index(':precondition')    
    index_dict = find_parens( data[index:] )
    data = data[index:]

    ind_list = sorted(list(index_dict.keys()))
    
    if "and" in data[ind_list[0]:ind_list[0]+4]:
        ind_list = ind_list[1:]
        
    preconditions = []
    previoud_ind = -1
    for ind in ind_list:
        if ind > previoud_ind:
            preconditions.append( data[ ind: index_dict[ind]+1] )
            previoud_ind = index_dict[ind]+1

    return preconditions

def get_effect(data):

    index = data.index(':effect')    
    index_dict = find_parens( data[index:] )
    data = data[index:]

    ind_list = sorted(list(index_dict.keys()))[1:]
    
    if "and" in data[ind_list[0]:ind_list[0]+4]:
        ind_list = ind_list[1:]

    effect = []
    previoud_ind = -1
    for ind in ind_list:
        if ind > previoud_ind:
            effect.append( data[ ind: index_dict[ind]+1] )
            previoud_ind = index_dict[ind]+1

    return effect

def get_actions(file):

    with open(file) as f:
        file_data = f.read()

        return_dict = {}

        list_of_action_index = [ item.start() for item in re.finditer(pattern='\(:action', string=file_data) ]
        for action_index in list_of_action_index:
            action_closing_ind = find_parens( file_data[action_index:] )[0]
            temp_data = file_data[action_index: action_index + action_closing_ind+1]

            action_name = str(temp_data.split('\n')[0]).split(' ')[-1]
            parameters = get_params(temp_data)
            preconditions = get_preconditions(temp_data)
            effect = get_effect(temp_data)

            return_dict[action_name] = {}
            return_dict[action_name]["parameters"] = parameters["parameters"]
            return_dict[action_name]["preconditions"] = preconditions
            return_dict[action_name]["effect"] = effect

        return return_dict
