#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./satellite/generator_single.sh" to generate an instance

mainPath="satellite/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"

# Define the different configurations
declare -a nsatel=(1 2 3 4 5 6 7 8 9 10 12 13 15)
declare -a instruments=(3)
declare -a modes=(3 4 5 6 7 8)
declare -a targets=(7 8 10 11 28 19 20 25 43 53 75 105)
declare -a observations=(3 4 5 6 10 15 20 34 40 47 66 87 93)

#Select a random configuration
nsatelSize=${#nsatel[@]}
nsatelIndex=$(($RANDOM % $nsatelSize))
instrumentsSize=${#instruments[@]}
instrumentsIndex=$(($RANDOM % $instrumentsSize))
modesSize=${#modes[@]}
modesIndex=$(($RANDOM % $modesSize))
targetsSize=${#targets[@]}
targetsIndex=$(($RANDOM % $targetsSize))
observationsSize=${#observations[@]}
observationsIndex=$(($RANDOM % $observationsSize))

declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done

nsatelVal=${nsatel[$nsatelIndex]}
instrumentsVal=${instruments[$instrumentsIndex]}
modesVal=${modes[$modesIndex]}
targetsVal=${targets[$targetsIndex]}
observationsVal=${observations[$observationsIndex]}

problem_file=$tmpFolder"/problem_satellite_$nsatelVal_$instrumentsVal_$modesVal_$targetsVal_$observationsVal_$c.pddl"
            
output=$(./"$mainPath"satgen $c $nsatelVal $instrumentsVal $modesVal $targetsVal $observationsVal)
echo "$output" > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"