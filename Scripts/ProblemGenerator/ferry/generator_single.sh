#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./ferry/generator_single.sh" to generate an instance

mainPath="ferry/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"

declare -a locations=(4 5 6)
declare -a cars=(3 4 5 6)

#Select a random configuration
locSize=${#locations[@]}
locIndex=$(($RANDOM % $locSize))
carsSize=${#cars[@]}
carsIndex=$(($RANDOM % $carsSize))


declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done

locVal=${locations[$locIndex]}
carsVal=${cars[$carsIndex]}

problem_file=$tmpFolder"/problem_ferry_$locVal_$carsVal_$c.pddl"
            
output=$(./"$mainPath"ferry -l $locVal -c $carsVal -s $c)
echo "$output" > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"