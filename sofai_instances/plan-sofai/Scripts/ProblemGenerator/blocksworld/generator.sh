#!/bin/bash

# Check if the problem_files folder exists, if not create it
if [ ! -d "problem_files" ]; then
  mkdir "problem_files"
fi

# Assuming the domain file is located in the current directory
domain_file="4ops/domain.pddl"

for num in {4..18}; do
    echo "Generating problems for configuration: ops - 4; num - $num"

    # Counter for successful problem generations
    counter=1

    # Generate 1200 executions for this configuration, using the loop index as the seed
    while [ $counter -le 1200 ]; do
        # Execute the program with the given configuration parameters and seed
        output=$(./blocksworld.sh 4 "$num")
        problem_file="problem_files/problem_${num}_${counter}.pddl"
        echo "$output" > "$problem_file"

        # Generate prompt for the problem
        prompt=$(python plansformer_prompt_generator.py "$domain_file" "$problem_file")

        # Count tokens in the prompt
        token_count=$(python count_512subset.py "$prompt")
        
        echo "$token_count tokens in problem_${num}_${counter}.pddl, generated...\r"
        
        counter=$((counter + 1))
    done
done
