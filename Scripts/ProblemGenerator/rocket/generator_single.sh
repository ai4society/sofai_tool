#!/bin/bash
#!/usr/bin/env python3

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./rocket/generator_single.sh" to generate an instance

mainPath="rocket/"
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



problem_found=0

while [ $problem_found -eq 0 ]; do

  declare -a rockets=(1 2 3 4 5 6 7 8 9 10)
  declare -a locations=(2 3 4 5 6 7 8 9 10) #(1 2 3 4 5)

  #Select a random configuration
  rocketsSize=${#rockets[@]}
  rocketsIndex=$(($RANDOM % $rocketsSize))
  locationsSize=${#locations[@]}
  locationsIndex=$(($RANDOM % $locationsSize))

  rocketsVal=${rockets[$rocketsIndex]}
  locationsVal=${locations[$locationsIndex]}

  problem_file="$tmpFolder"/problem_rocket_"$rocketsVal"_"$locationsVal"_"$c".pddl
              
  #python "$mainPath"single_generation_script.py "$rocketsVal" "$locationsVal" > "$problem_file"
  output=$(python3 "$mainPath"single_generation_script.py "$rocketsVal" "$locationsVal")

  outputContent=$(cat $output)
  if [[ $outputContent == *"GENERATION FAILURE"* ]]; then
    #echo "Not Found with "$rocketsVal" rockets and "$locationsVal" locations"
    problem_found=0
  else
    problem_found=1
    for file in $(find $tmpFolder -type f); do
      if cmp --silent -- "$output" "$file"; then
        problem_found=0
        break
      fi
    done

    if [ $problem_found -eq 1 ]; then
      mv "$output" "$problem_file"
      echo "$domain_file" "$problem_file"
    fi

  fi
done


#Print out domain and instance name to feed the next script
