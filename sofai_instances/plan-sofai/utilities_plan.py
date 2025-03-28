import re
import os

'''Function that parses some basic values from utilities files (i.e., threshold and contex)'''
def getVarFromFile(filename,varname):
    with open(filename) as myfile:
        for line in myfile:
            if ":"+varname in line:
                line = re.sub(r';.*$', '', line)
                discard, var = line.partition(":"+varname)[::2]
                var = var.replace(")", "")
                myfile.close()
                return var.strip()
        raise Exception('Missing variable named '+ varname)
    raise Exception('Missing file named '+ filename)

'''Function that parses some basic values from utilities files and does not discard comments (i.e., threshold and contex)'''
def getVarFromFile_comment(filename,varname):
    with open(filename) as myfile:
        for line in myfile:
            if ":"+varname in line:
                discard, var = line.partition(":"+varname)[::2]
                var = var.replace(")", "")
                myfile.close()
                return var.strip()
        raise Exception('Missing variable named '+ varname)
    raise Exception('Missing file named '+ filename)

'''Function that parses the tmp file that stores the solution from any solving process
We assume that every solver (System-1 or System-2) generates this temporary file with the solution
'''
def readSolutionFromFile(filename, solver):
    try:
        if solver == 0: # System-1 plansformer and FD
            with open(filename) as myfile:
                for line in myfile:
                    if "Solution" in line:
                        if '=' in line:
                            discard, sol = line.partition("=")[::2]
                            res=[]
                            #sol = sol.replace(' ','')
                            sol = sol.replace(';','')
                            sol = sol.replace('\n','')

                            acts = sol.split(',')

                            for act in acts:
                                if act and not act.isspace():
                                    res.append(act.strip())

                            myfile.close()
                            return res
        elif solver == 1: # LPG
            with open(filename) as myfile:
                res=[]
                for line in myfile:
                    if "no solution" in line:
                        return "noSolution"
                    else:
                        cleanedLine = re.sub(r'(.*);.*',r'\1',line)
                        cleanedLine = cleanedLine.strip()
                        #print(f"Cleaned line --- {cleanedLine}")
                        if '(' in cleanedLine:
                            res.append(re.sub(r'.*\((.+)\).*',r'\1',cleanedLine).lower())
                return res

        #raise Exception('Missing solution in '+ filename)
        else:
            return "noSolution"
    except IOError:
        return "noSolution"

'''Function that parses the tmp file that stores the time from any solving process
We assume that every solver (System-1 or System-2) generates this temporary file with the solving time
'''
def readTimeFromFile(filename):
    with open(filename) as myfile:
        for line in myfile:
            if "TIMED-OUT" in line:
                return "TO"
            elif "completed the search" in line or "Search time" in line:
                if ':' in line:
                    discard, ret = line.partition(":")[::2]
                    ret = ret.replace(' ','')
                    ret = ret.replace('\n','')
                    ret = ret.replace('s','')
                    ret = ret.strip()
                    
                    return ret

    #raise Exception('Missing plan in '+ filename)
    return "TO"

'''Function that parses sthe optimal plan length in file'''
def readOptLenghtFromFile(filename):
    try:
        return getVarFromFile_comment(filename,"optlen")
    except:
        return -1

'''Function that cleans the solution generated by Plansformer to retrieve the actual info (i.e., the solution and the confidence)'''
def tensor_clean(to_clean):
    ret = re.sub(r'tensor\(([\d \.]+),(.+)\)', r'\1', str(to_clean))
    ret = re.sub(r'tensor\((.+)\)', r'\1', str(ret))
    return ret


id_merger= "--UNIQUEIDMERGER--" 
'''Function that merges problem and domain name in an unique id'''
def unify_names(problem_name,domain_name):
    return problem_name + id_merger + domain_name

'''Function that splits problem and domain name from the unique id'''
def split_names(problem_id):
    if id_merger in problem_id:
        parts = problem_id.split(id_merger, 1)
        return parts[0], parts[1]
    return problem_id, ""

"""Iterates over files in the subfolder and return a list with their filenames with full paths if they have a .pddl extension."""
def list_files_in_folder(files_path,subfolder):
    ret_list = []
    files_path = os.path.join(files_path, subfolder)
    if not os.path.exists(files_path):
        print(f"The '{files_path}' folder does not exist.")
        return ret_list
    
    for root, _, files in os.walk(files_path):
        for file in files:
            if file.endswith(".pddl"):
                file_path = os.path.join(root, file)
                ret_list.append(file_path)
    
    return ret_list
