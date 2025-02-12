import sys
import re

if __name__ == "__main__":
    filename = sys.argv[1]
  	
   # Read data from file
    with open(filename, 'r') as file:
        lines = file.readlines()

    plan=""
    for line in lines:
        if ":solution" in line:
            plan = re.sub(r".*\(:solution (.*)\).*", r"\1", line)
    
    
    #plan_filename="planForToken.tmp"
    #with open(plan_filename, 'w') as file:
    #    file.write(plan)
   
    print(plan)