#!/bin/bash

# Script to generate a problem file with $1 number of blocks.
# Usage from the "Scripts/ProblemGenerator" folder execute "./blocksworld/generator_single.sh 10" to generate an instance with 10 blocks

mainPath="blocksworld/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"4ops/domain.pddl"

num=$1

# Execute the program with the given configuration parameters and seed
output=$(./"$mainPath"blocksworld.sh 4 "$num")

declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done


problem_file=$tmpFolder"problem_bw_${num}_${c}.pddl"
echo "$output" > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"