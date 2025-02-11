import re
import sys
import time

# Function that parses some basic values from the threshold file
def get_var_from_file(filename, varname):
    with open(filename, 'r') as myfile:
        for line in myfile:
            line = line.strip()
            # Skip comments and empty lines
            if line.startswith("#") or not line:
                continue
            # Match key-value pairs with optional comments at the end
            match = re.match(rf"{varname}\s*=\s*([^#]+)", line)
            if match:
                return match.group(1).strip()  # Return the value part, stripped of whitespace
        raise Exception(f"Missing variable named '{varname}' in file '{filename}'.")

# Function that parses the Threshold file
def read_threshold(thresholdFile):
    threshold1 = float(get_var_from_file(thresholdFile, "threshold1"))
    threshold2 = float(get_var_from_file(thresholdFile, "threshold2"))
    threshold3 = float(get_var_from_file(thresholdFile, "threshold3"))
    threshold4 = float(get_var_from_file(thresholdFile, "threshold4"))
    epsilon_s1 = float(get_var_from_file(thresholdFile, "epsilonS1"))
    correctness_threshold = float(get_var_from_file(thresholdFile, "correctness_threshold"))
    time_limit = int(get_var_from_file(thresholdFile, "time_limit"))
    max_experience = int(get_var_from_file(thresholdFile, "maxExperience"))

    return threshold1, threshold2, threshold3, threshold4, epsilon_s1


'''Utility function that ends the computation'''
def end_computation(problemId,timerComputation):
    print(f"Problem {problemId} could not be solved in {(time.time() - timerComputation)}ms")
    sys.exit()