#!/bin/bash

# Specify the path to the domain file
domain_file="domain.pddl"

# Check if the problem_files folder exists, if not create it
if [ ! -d "problem_files" ]; then
  mkdir "problem_files"
fi

declare -a locations=(4 5 6)
declare -a cars=(3 4 5 6)

for ((i=0; i<${#locations[@]}; i++)); do
    for ((j=0; j<${#cars[@]}; j++)); do
        echo "Generating ferry problem configuration with ${locations[$i]} locations and ${cars[$j]} cars"
        counter=1
        while [ $counter -le 1500 ]; do
            # Generate a unique filename for each problem file
            problem_file="problem_files/problem_${locations[$i]}_${cars[$j]}_$counter.pddl"
            
            # Generate the problem file with the given configuration
            output=$(./ferry -l ${locations[$i]} -c ${cars[$j]} -s $counter)
            echo "$output" > "$problem_file"

            # Generate prompt for the problem
            prompt=$(python plansformer_prompt_generator.py "$domain_file" "$problem_file")

            # Count tokens in the prompt
            token_count=$(python count_512subset.py "$prompt")

            # Print the token count for the generated problem
            echo "$token_count tokens in $problem_file, generated..."

            counter=$((counter + 1))
            echo -ne "\t${counter}/1500 problems generated\r"
        done
    done
done


# # Loop over each combination of location and car numbers
# for c in "${combinations[@]}"; do
#   # Extract the location and car numbers
#   l=$(echo $c | awk '{print $1}')
#   cars=$(echo $c | awk '{print $2}')

#   # Generate 1200 executions for this combination, using the loop index as the seed
#   for i in $(seq 1 1500); do
#     # Execute the program with the given location and car numbers and seed, and capture the output
#     output=$(./ferry -l $l -c $cars -s $i)

#     # Create the problem file name and write the output to the file
#     problem_file="problem_${l}_${cars}_${i}.pddl"
#     echo -e "$output" > "problem_files/$problem_file"
#   done
# done