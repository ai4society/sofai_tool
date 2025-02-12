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

def prompt_action(data):

    # print(data)
    string = '<ACTION> ' + data.split('\n')[0].split(' ')[1].lower() + ' '

    if ':precondition' in data:
        string += '<PRE> '
        pre_idx = data.find(':precondition')
        effect_idx = data.find(':effect')
        pre_data = data[pre_idx:effect_idx]
        pre_parens = find_parens(pre_data)
        # print(pre_data)
        for keys in sorted(pre_parens.keys()):
            temp_str = pre_data[keys:pre_parens[keys]+1]
            if '(and' not in temp_str:
                string += temp_str.strip('(').strip(')').replace('?', '') + ', '

        string = string[:-2] + ' '
        # print(string)

    if ':effect' in data:
        string += '<EFFECT> '
        effect_idx = data.find(':effect')
        effect_data = data[effect_idx:]
        effect_parens = find_parens(effect_data)

        check_st = 0
        check_end = 0
        flag = 0
        flag_forall = 0
        for keys in sorted(effect_parens.keys()):
            temp_str = effect_data[keys:effect_parens[keys]+1]

            if '(forall' in temp_str[:8] and '(and' not in temp_str[:5]:
                for ind in range(len(temp_str)):
                    if ind < len(temp_str) - 2:
                        if temp_str[ind] == ')' and temp_str[ind+2] == '(':
                            temp_str = temp_str[:ind] + ', '+ temp_str[ind+2:]

                string += '(' + temp_str.replace('?', '').replace('(','').replace(')','').replace('and', '').replace('\n', ',').strip() + ')' + ', '
                flag_forall = 1

            elif flag_forall == 0:
                if flag == 1:
                    if keys > check_st and keys < check_end:
                        continue

                if '(and' not in temp_str:
                    string += temp_str.replace('(', '').replace(')', '').replace('?', '') + ', '

                    if '(not' in temp_str:
                        flag = 1
                        check_st = keys
                        check_end = effect_parens[keys]

        string = string[:-2] + ' '

    return string


def prompt_problem( data ):

    if '(:init' in data:
        string = '<INIT>'

        parens = find_parens(data)
        check_st = 0
        check_end = 0
        flag = 0

        for keys in sorted(parens.keys()):
            temp_str = data[keys:parens[keys]+1]

            if flag == 1:
                if keys > check_st and keys < check_end:
                    continue

            if '(:init' not in temp_str:
                string += temp_str.replace('(', '').replace(')', '') + ', '

                if '(not' in temp_str:
                    flag = 1
                    check_st = keys
                    check_end = parens[keys]

        return string[:-2] + ''

    elif '(:goal' in data:
        string = '<GOAL>'

        parens = find_parens(data)
        check_st = 0
        check_end = 0
        flag = 0

        for keys in sorted(parens.keys()):
            temp_str = data[keys:parens[keys]+1]

            if flag == 1:
                if keys > check_st and keys < check_end:
                    continue

            if ('(:goal' and '(and') not in temp_str:
                string += temp_str.replace('(', '').replace(')', '') + ', '

                if '(not' in temp_str:
                    flag = 1
                    check_st = keys
                    check_end = parens[keys]

        return string[:-2] + ''


def get_prompt(domain_file, problem_file):
    with open(domain_file, 'r') as f:
        domain_data = f.read()

    domain_name = re.findall(r'(?<=domain )\w+', domain_data)
    domain_name = domain_name[0]

    flag = 1

    idx = [m.start() for m in re.finditer(pattern=':action', string=domain_data)]

    domain_string = ''

    for id in range(len(idx)):
        if id != len(idx) - 1:
            domain_string += prompt_action(domain_data[idx[id]-1: idx[id+1]-1]).strip() + ' '
        else:
            domain_string += prompt_action(domain_data[idx[id]-1:])

    with open(problem_file, 'r') as f:
        problem_data = f.read()


    init_ind = problem_data.find('(:init')
    goal_ind = problem_data.find('(:goal')

    problem_string = ''
    problem_string += prompt_problem( problem_data[goal_ind:] )
    problem_string += prompt_problem( problem_data[init_ind:goal_ind] )

    return problem_string + domain_string