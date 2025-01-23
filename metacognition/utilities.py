import re

'''Function that parses some basic values from utilities files (i.e., threshold and contex)'''
def get_var_from_file(filename,varname):
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


'''Function that parses the Threshold file'''
def read_threshold(thresholdFile):
    threshold1 = float(get_var_from_file(thresholdFile,"threshold1"))
    threshold2 = float(get_var_from_file(thresholdFile,"threshold2"))
    threshold3 = float(get_var_from_file(thresholdFile,"threshold3"))
    threshold4 = float(get_var_from_file(thresholdFile,"threshold4"))
    epsilon_s1  = float(get_var_from_file(thresholdFile,"epsilonS1"))
    
    return threshold1,threshold2,threshold3,threshold4,epsilon_s1