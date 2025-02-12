#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./hanoi/generator_single.sh" to generate an instance

mainPath="hanoi/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"

declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done


problem_file="$tmpFolder"/problem_"hanoi"_"$c".pddl
            
python "$mainPath"single_generation_script.py "5" > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"