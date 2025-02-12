import os
import subprocess
import signal
import time

# Set the paths to the domain file, problem files folder, and output folder
domain_file = "domain.pddl"
problem_files_folder = "problem_files"
output_folder = "plans"

planner_path = "/Users/bittu/Desktop/GitHub/downward"

# Create the output folder if it doesn't already exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop over all the problem files in the problem files folder
count = 0
start_time = time.time()
for problem_file_name in os.listdir(problem_files_folder):
    count += 1
    print("Generating Plan for Problem " + str(count) + ": " + problem_file_name, end="\r")
    # Construct the input and output file paths
    problem_file_path = os.path.join(problem_files_folder, problem_file_name)
    output_file_path = os.path.join(output_folder, problem_file_name.replace("problem", "plan").replace(".pddl", ".txt"))

    # Call the Fast-Downward planner to generate a plan for the current problem file
    # process = subprocess.Popen([planner_path + "/fast-downward.py", "--plan-file", output_file_path, "--alias", "seq-sat-lama-2011", "--overall-time-limit", "2m" ,domain_file, problem_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen([planner_path + "/fast-downward.py", "--plan-file", output_file_path,domain_file, problem_file_path, "--search", "astar(lmcut())"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    output, error = process.communicate()
    if os.path.exists(output_file_path) == False:
        print("Error in generating plan for problem: " + problem_file_name)
        print("Error: " + error.decode())

    # while not os.path.exists(output_file_path + ".1"):
    #     returncode = process.poll()
    #     if returncode is not None:
    #         # Process has finished, print any error messages and exit the loop
    #         output, error = process.communicate()
    #         if error:
    #             print(f"Error messages at {problem_file_name}:")
    #             print(error.decode())
    #         break
        

    # process.kill()
    # process = subprocess.Popen([planner_path + "/fast-downward.py", "--plan-file", output_file_path, domain_file, problem_file_path, "--search", "astar(lmcut())"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    # # Kill the process if it is still running
    # if process.poll() is None:
    #     process.terminate()
    # output, error = process.communicate()

    # # Print the error messages, if any
    # if error:
    #     print(f"Error messages at {problem_file_name}:")
    #     print(error.decode())
end_time = time.time()
print("Time taken: " + str(end_time - start_time) + " seconds")
