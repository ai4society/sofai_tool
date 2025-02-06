#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./grippers/generator_single.sh" to generate an instance

mainPath="grippers/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"

declare -a robots=(2 3)
declare -a rooms=(2 3 4 5)
declare -a balls=(3 4 5)

#Select a random configuration
robotsSize=${#robots[@]}
robotsIndex=$(($RANDOM % $robotsSize))
roomsSize=${#rooms[@]}
roomsIndex=$(($RANDOM % $roomsSize))
ballsSize=${#balls[@]}
ballsIndex=$(($RANDOM % $ballsSize))

declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done

robotsVal=${robots[$robotsIndex]}
roomsVal=${rooms[$roomsIndex]}
ballsVal=${balls[$ballsIndex]}

problem_file="$tmpFolder"/problem_gr_"$robotsVal"_"$roomsVal"_"$ballsVal"_"$c".pddl
            
python "$mainPath"single_generation_script.py $robotsVal $roomsVal $ballsVal "1"> "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"