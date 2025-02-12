#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./barman/generator_single.sh" to generate an instance

mainPath="barman/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"

# Define the different configurations
declare -a cocktails=(2 3 4 5 6)
declare -a ingredients=(2 3 4) #(1 2 3 4 5)
declare -a shots=(1 2 3) #(1 2 3 4)

#Select a random configuration
cocktailsSize=${#cocktails[@]}
cocktailsIndex=$(($RANDOM % $cocktailsSize))
ingredientsSize=${#ingredients[@]}
ingredientsIndex=$(($RANDOM % $ingredientsSize))
shotsSize=${#shots[@]}
shotsIndex=$(($RANDOM % $shotsSize))


declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done

cocktailsVal=${cocktails[$cocktailsIndex]}
ingredientsVal=${ingredients[$ingredientsIndex]}
shotsVal=$(( cocktailsVal+${shots[$shotsIndex]} ))

#echo -e "Cocktails: $cocktailsVal\nIngredients: $ingredientsVal\nShots: $shotsVal ($cocktailsVal + ${shots[$shotsIndex]})"

problem_file=$tmpFolder"/problem_barman_$cocktailsVal_$ingredientsVal_$shotsVal_$c.pddl"
            
python3 "$mainPath"barman-generator.py  $cocktailsVal $ingredientsVal $shotsVal $c > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"
