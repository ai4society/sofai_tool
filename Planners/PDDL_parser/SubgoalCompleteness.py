import os

def convert_string_to_list(input_string):
    conditions = input_string.split("(and")[-1]
    conditions = conditions.split(') (')
    conditions = [c.replace('(not ', 'not ') if c.startswith('(not ') else c for c in conditions]
    conditions = [c[:-1] if c.endswith(')') else c for c in conditions]
    return [i.replace("(","").replace(")", "").strip() for i in conditions]

def remove_empty(list_inp):
    return [i for i in list_inp if len(i)!=0]

import re

def read_domain(path):
    file1 = open(path, 'r')
    lines = file1.readlines()
    dict_act = dict()
    for i in range(len(lines)):
        if re.match(r"\s*\(:action", lines[i]):
            act = lines[i].split(' ')[-1].replace("\n", "")
            dict_act[act] = [0, [],[]]

        elif re.match(r"\s*:parameters", lines[i]):
            all_text = lines[i]
            for j in range(i+1, len(lines)):
                if re.match(r"\s*:precondition", lines[j]):
                    break
                else:
                    all_text = all_text + lines[j]
                    continue
            # print(all_text)
            all_text = all_text.strip()
            if '\n' in all_text:
                # If input_string contains parameter names in parentheses
                parameter_list = []
                for line in all_text.strip().split('\n'):
                    # print(line)
                    # raise KeyboardInterrupt
                    if 'parameters' not in line:
                        parameter_list.append(line.strip().split()[0])
            else:
                # If input_string contains parameter names as separate lines
                parameters = all_text.split('(', 1)[1].split(')')[0].strip()
                # print(parameters)
                # raise KeyboardInterrupt
                if parameters == '':
                    parameter_list = []
                else:
                    parameter_list = parameters.split()
            parameter_list = [i.replace("(","") for i in parameter_list if i.count("?")]
            # print(parameter_list)
            # raise KeyboardInterrupt
            dict_act[act][0] = all_text.count("?")
            dict_act[act][1] = dict_act[act][1] + parameter_list

        elif re.match(r"\s*:effect", lines[i]):
            temp_list = list()
            flag_update = False
            for j in range(i, len(lines)):
                if lines[j].count("effect:"):
                    if lines[j].count("("):
                        temp_list = temp_list + convert_string_to_list(lines[j].split("effect:")[1])
                    else:
                        continue
                elif re.match(r"\s*\(:action", lines[j]):
                    dict_act[act][2] = dict_act[act][2] + remove_empty(temp_list)
                    flag_update = True
                    break
                else:
                    temp_list = temp_list + convert_string_to_list(lines[j])
            if flag_update==False:
                dict_act[act][2] = dict_act[act][2] + remove_empty(temp_list)
        else:
            continue

    new_dict = dict()
    for i in dict_act.keys():
        if str(dict_act[i][0]) not in new_dict.keys():
            new_dict[str(dict_act[i][0]).lower()] = dict()
            new_dict[str(dict_act[i][0]).lower()][i.lower()] = [dict_act[i][1], dict_act[i][2]]
        else:
            new_dict[str(dict_act[i][0]).lower()][i.lower()] = [dict_act[i][1], dict_act[i][2]]
    return new_dict

def read_plan(plan_text):
    plan = plan_text.split(",")
    # print(f"\nDEBUG HERE with plan: {plan}\n")
    # stripping extra whitespace in the start and the end
    plan = [i.strip() for i in plan]
    # print(f"\nDEBUG HERE with plan: {plan}\n")
    # raise KeyboardInterrupt
    plans = list()
    for j in range(len(plan)):
        if plan[j].count("not")==0:
            temp = plan[j].split(" ")
            plans.append([len(temp)-1] + temp)
        else:
            temp = plan[j].split(" ")
            plans.append([len(temp)-2] + [" ".join(temp[:2])] + temp[2:])

    new_plan = list()
    for i in plans:
        if "not" in " ".join([str(j) for j in i]):
            new_plan.append((str(i[0])," ".join(i[1:3])," ".join(i[1:])))
        else:
            new_plan.append((str(i[0])," ".join(i[1:2])," ".join(i[1:])))
    new_plan = [i for i in new_plan if len(i[1])>0 and len(i[2])>0]
    return new_plan

def read_init(path):
    file1 = open(path, 'r')
    lines = file1.readlines()
    init_cond = list()
    for i in range(len(lines)):
        # if lines[i].startswith('(:init'):
        if re.match(r"\s*\(:init", lines[i]):
            for j in range(i+1, len(lines)):
                # if lines[j].startswith('(:goal'):
                if re.match(r"\s*\(:goal", lines[j]):
                    break
                if re.match(r"\s*\(", lines[j]) and lines[j].count("and")==0:
                    temp = lines[j].replace("(","").replace(")","").replace("\n", "")
                    if temp.count("not")==0:
                        temp = temp.split(" ")
                        init_cond.append([len(temp)-1] + temp)
                    else:
                        temp = temp.split(" ")
                        init_cond.append([len(temp)-2] + [" ".join(temp[:2])] + temp[2:])
        else:
            continue

    new_init = list()
    for i in init_cond:
        if "not" in " ".join([str(j) for j in i]):
            new_init.append((str(i[0])," ".join(i[1:3])," ".join(i[1:])))
        else:
            new_init.append((str(i[0])," ".join(i[1:2])," ".join(i[1:])))

    return [i[2].replace("\t","") for i in new_init]

def read_goal(path):
    file1 = open(path, 'r')
    lines = file1.readlines()
    goal = list()
    for i in range(len(lines)):
        # if lines[i].startswith('(:goal'):
        if re.match(r"\s*\(:goal", lines[i]):
            # print(f"\nDEBUG HERE with Lines: {lines[i]}\n")
            flag_end = False
            for j in range(i+1, len(lines)):
                # print(f"\nDEBUG HERE with Lines: {lines[j]}\n")
                if re.match(r"\s*\(", lines[j]) and lines[j].count("and")==0:
                    # print(f"\nDEBUG HERE with Lines: {lines[j]}\n")
                    temp = lines[j].replace("(","").replace(")","").replace("\n", "")
                    # print(f"\nDEBUG HERE with Lines processed: {temp}\n")
                    if temp.count("not")==0:
                        temp = temp.strip().split(" ")
                        # print(temp, len(temp))
                        goal.append([len(temp)-1] + temp)
                    else:
                        temp = temp.split(" ")
                        # print(temp, len(temp))
                        goal.append([len(temp)-2] + [" ".join(temp[:2])] + temp[2:])
                if lines[j].count(")"):
                    flag_end = True
                elif lines[j].startswith(' ') and flag_end==True:
                    # print("I am here")
                    # print(j, lines[j])
                    break
        else:
            continue
    # print(goal)
    new_goal = list()
    for i in goal:
        if "not" in " ".join([str(j) for j in i]):
            new_goal.append((str(i[0])," ".join(i[1:3])," ".join(i[1:])))
        else:
            new_goal.append((str(i[0])," ".join(i[1:2])," ".join(i[1:])))

    return new_goal

def check_not(final_state, temp):
    new_state = list()
    for i in final_state:
        if i.count("not")>0:
            if i.replace("not ","") in temp:
                continue
            else:
                new_state.append(i)
        else:
            if "not "+i in temp:
                continue
            else:
                new_state.append(i)
    return new_state

def subgoal_completeness(goal, plan, domain, init_cond):
    final_state = init_cond.copy()
    # print(init_cond)
    #print(f"\nDEBUG HERE with plan: {plan}\n")
    #print(f"\nDEBUG HERE with init: {init_cond}\n")
    #print(f"\nDEBUG HERE with goal: {goal}\n")

    for i in plan:
        # print(i)
        if i[0] not in list(domain.keys()):
            # print("No changes required others")
            return 0
        elif i[1] not in list(domain[i[0]].keys()):
            # print("No changes required domain")
            # print(i[0], i[1], list(domain[i[0]].keys()))
            return 0
        else:
            temp = domain[i[0]][i[1]]
            parameter = list()
            for j in range(int(i[0])):
                parameter.append(i[2].split(" ")[j+1])
            changes  = temp[0]
            temp = temp[1]
            if len(changes)==0:
                print("No changes required")
            else:
                update_temp = list()
                for sub_text in temp:
                    tmp_txt = sub_text + " "
                    for m,n in zip(changes, parameter):
                        # print(tmp_txt)
                        # if tmp_txt.count(m+" "):
                        tmp_txt = tmp_txt.replace(m+" ",n+" ")
                        # else:
                            # tmp_txt = tmp_txt.replace(m,n)
                    update_temp.append(tmp_txt.strip())
                temp = update_temp
            # print(update_temp)
            if len(final_state)!=0:
                final_state = check_not(final_state, temp)
            for g in temp:
                final_state.append(g)
    count = 0
    for i in goal:
        if i[2] in final_state:
            count += 1
        else:
            continue
    return count/len(goal)

def get_correctness(domain_path, plan_text, instance_path):
    domain  = read_domain(domain_path)
    # print(f"\nDEBUG HERE with domain: {domain}\n")

    ######################@TODO: DEBUG ROCKET SPECIFIC
    pre, ext = os.path.splitext(instance_path)
    pf_problem_file =(f'{pre}.formatted')
    with open(instance_path, 'r') as file:
        data = file.read()
    data = re.sub(r"(\(.+\)) (\(.+\))", r"\1\n\2", data)
    
    with open(pf_problem_file, 'w') as file:
        file.write(data)
    ######################@TODO: DEBUG ROCKET SPECIFIC


    plan = read_plan(plan_text)
    #print(f"\nDEBUG HERE with plan: {plan}\n")
    goal = read_goal(pf_problem_file)
    #print(f"\nDEBUG HERE with goal: {goal}\n")
    init_cond = read_init(pf_problem_file)
    #print(f"\nDEBUG HERE with init: {init_cond}\n")
    return subgoal_completeness(goal, plan, domain, init_cond)

# plan_text = "fuelup r0 l0,load c2 r0 l0,fly r0 l1,unload c2 r0 l1,fuelup r0 l1,load c0 r0 l1,fly r0 l2,unload c0 r0 l2,fuelup r0 l2,load c1 r0 l2,fly r0 l0,unload c1 r0 l0"
# plan_text_hn = "move d2 d3 d4, move d1 peg2 d2, move d3 peg1 peg2, move d1 d2 peg1, move d2 d4 d3, move d1 peg1 d2, move d4 d5 peg1, move d1 d2 d4, move d2 d3 d5, move d1 d4 d2, move d3 peg2 d4, move d1 d2 peg2, move d2 d5 d3, move d1 peg2 d2, move d5 peg3 peg2, move d1 d2 peg3, move d2 d3 d5, move d1 peg3 d2, move d3 d4 peg3, move d1 d2 d4, move d2 d5 d3, move d1 d4 d2, move d4 peg1 d5, move d1 d2 d4, move d2 d3 peg1, move d1 d4 d2"
# print(get_correctness("domain_test.pddl", plan_text, "problem.pddl"))
# print(get_correctness("domain_hn.pddl", plan_text_hn, "problem_hn.pddl"))