#!/bin/bash

# Specify the path to the domain file
domain_file="domain.pddl"

# Check if the problem_files folder exists, if not create it
if [ ! -d "problem_files" ]; then
  mkdir "problem_files"
fi

# Define the list of configurations
configurations=(
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

# Loop over each configuration
for c in "${configurations[@]}"; do
  # Extract the configuration parameters
  road_junctions=$(echo $c | awk '{print $1}')
  drivers=$(echo $c | awk '{print $2}')
  packages=$(echo $c | awk '{print $3}')
  trucks=$(echo $c | awk '{print $4}')
  distance=""

  echo "Generating problems for configuration: road-junctions - $road_junctions; drivers - $drivers; packages - $packages; trucks - $trucks"

  # Counter for successful problem generations
  counter=1

  # Generate 1200 executions for this configuration, using the loop index as the suffix
  while [ $counter -le 1200 ]; do
    # Generate the filename based on the configuration parameters and counter
    problem_file="problem_files/problem_${road_junctions}_${drivers}_${packages}_${trucks}_${counter}.pddl"

    # Execute the program with the given configuration parameters
    output=$(./dlgen $counter $road_junctions $drivers $packages $trucks $distance)
    echo "$output" > "$problem_file"

    # Generate prompt for the problem
    prompt=$(python plansformer_prompt_generator.py "$domain_file" "$problem_file")

    # Count tokens in the prompt
    token_count=$(python count_512subset.py "$prompt")

    # Print the token count for the generated problem
    echo "$token_count tokens in $problem_file, generated..."
        
    counter=$((counter + 1))
  done
done
