import Planners.PDDL_parser.domain_functions as df
import Planners.PDDL_parser.problem_functions as pf

#domain_file_path = "C:\\Users\\muppa\\Desktop\\domain train data\\blockworld\\domain.pddl"
#problem_file_path = "C:\\Users\\muppa\\Desktop\\domain train data\\blockworld\\problems\\problem_2_1.pddl"

# fucntion gives required details modeled in classical pddl files

def get_details(domain_file, problem_file):
    domain_name = df.get_domain_name(domain_file).strip()
    problem_name = pf.get_problem_name(problem_file)[0].strip()
    init_States = pf.get_initialState(problem_file)
    goal_States = pf.get_goalState(problem_file)
    number_of_actions = len(df.get_actions(domain_file))
    number_of_predicates = len(df.get_predicates(domain_file))

    return domain_name, problem_name, init_States, goal_States, number_of_actions, number_of_predicates

def get_cleaned_actions(domain_file):

    ret_actions = []

    keys = [['preconditions','PRE'], ['effect','EFFECT']]
    chars_toReplace = ['(', ')', '?']

    actions = df.get_actions(domain_file)
    for act in actions:
        tmpact = "<ACTION> " + act
        for k in keys:
            if k[0] in actions[act]:
                tmpact += " <"+k[1]+"> "
                for elem in actions[act][k[0]][:-1]:
                    tmpact += elem + ", "
                tmpact += actions[act][k[0]][-1]

        for toRepl in chars_toReplace:
            tmpact = tmpact.replace(toRepl, "")
        ret_actions.append(tmpact)


    return ret_actions

def get_plansformer_description(domain_file, problem_file):

    init_States = pf.get_initialState(problem_file)
    goal_States = pf.get_goalState(problem_file)
    cleaned_actions = get_cleaned_actions(domain_file)


    description ="<GOAL>"
    for goal in goal_States[:-1]:
        description += goal + ", "
    description += goal_States[-1]

    description+="<INIT>"
    for init in init_States[:-1]:
        description += init + ", "
    description += init_States[-1]

    for act in cleaned_actions[:-1]:
        description += act + " "
    description += cleaned_actions[-1]


    return description

#print(get_details(domain_file_path, problem_file_path))
