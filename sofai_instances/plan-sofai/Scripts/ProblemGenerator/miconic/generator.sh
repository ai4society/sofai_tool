#!/bin/bash

# Specify the path to the domain file
domain_file="domain.pddl"

# Create the problem_files directory if it doesn't exist
if [ ! -d "problem_files" ]; then
    mkdir "problem_files"
fi

# Define the different configurations
declare -a floors=(6 7 8 9 10)
declare -a passengers=(4 5 6 7)

for ((i=0; i<${#floors[@]}; i++)); do
    for ((j=0; j<${#passengers[@]}; j++)); do
        echo "Generating elevator problem configuration with ${floors[$i]} floors and ${passengers[$j]} passengers"
        counter=1
        while [ $counter -le 900 ]; do
            # Generate a unique filename for each problem file
            problem_file="problem_files/problem_${floors[$i]}_${passengers[$j]}_$counter.pddl"
            
            # Generate the problem file with the given configuration
            output=$(./miconic -f ${floors[$i]} -p ${passengers[$j]} -r $counter)
            echo "$output" > "$problem_file"

            # Generate prompt for the problem
            prompt=$(python plansformer_prompt_generator.py "$domain_file" "$problem_file")

            # Count tokens in the prompt
            token_count=$(python count_512subset.py "$prompt")

            # Print the token count for the generated problem
            echo "$token_count tokens in $problem_file, generated..."

            counter=$((counter + 1))
            echo -ne "\t${counter}/900 problems generated\r"
        done
    done
done


# # Loop over each configuration
# for ((i=0; i<${#floors[@]}; i++)); do
#     echo "Generating elevator problem configuration with ${floors[$i]} floors and ${passengers[$i]} passengers"
#     for ((k=1; k<=1200; k++)); do
#         # Generate a unique filename for each problem file
#         filename="problem_files/problem_${floors[$i]}_${passengers[$i]}_$k.pddl"
#         # Generate the problem file with the given configuration
#         ./miconic -f ${floors[$i]} -p ${passengers[$i]} -r $k > $filename
#         echo -ne "\t${k}/1200 problems generated\r"
#     done
# done
