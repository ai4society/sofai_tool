#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./driverlog/generator_single.sh" to generate an instance

mainPath="driverlog/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"


# Define the list of configurations
declare -a configurations=(
  "5 2 2 2"
  "5 2 3 2"
  "5 2 4 2"
  "5 3 5 2"
  "5 3 5 3"
  "6 3 6 3"
  "6 3 7 3"
  "6 4 7 3"
  "6 4 8 4"
  "6 4 9 4"
  "7 5 9 4"
  "7 5 10 4"
  "7 5 10 5"
  "7 5 11 5"
  "7 5 12 5"
)

#Select a random configuration
configSize=${#configurations[@]}
index=$(($RANDOM % $configSize))

road_junctions=$(echo ${configurations[$index]} | awk '{print $1}')
drivers=$(echo ${configurations[$index]} | awk '{print $2}')
packages=$(echo ${configurations[$index]} | awk '{print $3}')
trucks=$(echo ${configurations[$index]} | awk '{print $4}')
distance=""

declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done


# Generate the filename based on the configuration parameters and counter
problem_file=$tmpFolder"problem_dl_${road_junctions}_${drivers}_${packages}_${trucks}_${c}.pddl"
# Execute the program with the given configuration parameters
output=$(./"$mainPath"dlgen $c $road_junctions $drivers $packages $trucks $distance)
echo "$output" > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"