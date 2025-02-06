#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./rovers/generator_single.sh" to generate an instance

mainPath="rovers/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"

# Define the different configurations
declare -a rovers=(1 3 5 7 8 9 10 12 14)
declare -a waypoints=(4 5 6 10 15 17 20 25 30 40 50)
declare -a objectives=(2 4 8 10 11)
declare -a cameras=(1 2 3 6 7 14 15)
declare -a ngoals=(1 2 3 4 5 10 11 12 13 20 25 40 45 50)

#Select a random configuration
roversSize=${#rovers[@]}
roversIndex=$(($RANDOM % $roversSize))
waypointsSize=${#waypoints[@]}
waypointsIndex=$(($RANDOM % $waypointsSize))
objectivesSize=${#objectives[@]}
objectivesIndex=$(($RANDOM % $objectivesSize))
camerasSize=${#cameras[@]}
camerasIndex=$(($RANDOM % $camerasSize))
ngoalsSize=${#ngoals[@]}
ngoalsIndex=$(($RANDOM % $ngoalsSize))

declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done

roversVal=${rovers[$roversIndex]}
waypointsVal=${waypoints[$waypointsIndex]}
objectivesVal=${objectives[$objectivesIndex]}
camerasVal=${cameras[$camerasIndex]}
ngoalsVal=${ngoals[$ngoalsIndex]}

problem_file=$tmpFolder"/problem_rovers_$roversVal_$waypointsVal_$objectivesVal_$camerasVal_$ngoalsVal_$c.pddl"
            
output=$(./"$mainPath"rovgen $c $roversVal $waypointsVal $objectivesVal $camerasVal $ngoalsVal)
echo "$output" > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"