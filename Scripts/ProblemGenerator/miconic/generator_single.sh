#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./miconic/generator_single.sh" to generate an instance

mainPath="miconic/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"

# Define the different configurations
declare -a floors=(6 7 8 9 10)
declare -a passengers=(4 5 6 7)

#Select a random configuration
floorsSize=${#floors[@]}
floorsIndex=$(($RANDOM % $floorsSize))
passengersSize=${#passengers[@]}
passengersIndex=$(($RANDOM % $passengersSize))


declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done

floorsVal=${floors[$locIndex]}
passengersVal=${passengers[$passengersIndex]}

problem_file=$tmpFolder"/problem_miconic_$floorsVal_$passengersVal_$c.pddl"
            
output=$(./"$mainPath"miconic -f $floorsVal -p $passengersVal -r $c)
echo "$output" > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"