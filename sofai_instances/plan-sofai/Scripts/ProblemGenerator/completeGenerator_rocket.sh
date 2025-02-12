#!/bin/bash
#!/usr/bin/env python3
# Script to generate $1 problem files for the domain for the BW (for each number fo blocks). These instances should require at least $2 seconds to be solved by the fastet planner we have and within $3 tries. $4 Activate (if == 1) optimality calculation
# Usage from the "Scripts/ProblemGenerator" folder execute "./completeGenerator_rocket.sh 20 0.01 100"
# Each instance will be below 512 token and should require more than 0.5 seconds to be solved by LPG. Finally, all domains will try to generate a maximum of 1000 instances and for each one the optiaml plan is calculated

max_tokens=512
outFolder="Output/"
dmnFolder="domain/"
instFolder="instances/"
minimumTime=$2
declare -i maxAttemptsPerDomain=$3

## now loop through the above array
domain="rocket/"

echo -e "\nWorking on $domain..."

tempDmnFolder=$outFolder$domain$dmnFolder
tempInstancesDir=$outFolder$domain$instFolder

mkdir -p $tempDmnFolder
mkdir -p $tempInstancesDir

declare -i attemptPerDomain=0
declare -i counter=0

while (($counter < $1 && $attemptPerDomain < $maxAttemptsPerDomain)); do

  result=$(./"$domain"/generator_single.sh "$blocksNum")

  seprated_res=($result)

  domain_file="${seprated_res[0]}"
  problem_file="${seprated_res[1]}"

  if [ -z "$(ls -A $tempDmnFolder)" ]; then
    cp $domain_file $tempDmnFolder/domain.pddl
  fi

  #This line splits the file name on the delimiter "."
  baseName=$(echo $problem_file | cut -d "." -f 1)
  newExtension=".clean"
  problem_file_cleaned="$baseName$newExtension"
  #Checking for token limitations
  tail -n +3 "$problem_file" > "$problem_file_cleaned"
  python3 rocket/remove_extra_init.py "$problem_file_cleaned"
  prompt=$(python3 plansformer_prompt_generator.py "$domain_file" "$problem_file_cleaned")
  rm $problem_file_cleaned
  token_count_problem=$(python3 count_512subset.py "$prompt")

  plan=$(python3 rocket/extract_plan.py "$problem_file")
  token_count_solution=$(python3 count_512subset.py "$plan")

  if [[ $token_count_problem -gt $token_count_solution ]]; then
      token_count=$token_count_problem
  else
      token_count=$token_count_solution
  fi

  #echo "Token total: $token_count, Token problem: $token_count_problem, Token solution: $token_count_solution"
  #echo "Plan is $plan"
  #rm $plan_file

  #token_count=100

  filename=$(basename -- "$problem_file")
  #Checking for token limitations
  if (($token_count <= $max_tokens)); then

    cp $problem_file $tempInstancesDir$filename
    counter=$((counter + 1))
    echo "Added problem $filename"
    python3 plansformer_csv_generator_rocket.py "$prompt" "$problem_file" "$outFolder$domain"

  else
    echo "Discarded problem $filename because of too many tokens"
    rm -f $problem_file
  fi

  attemptPerDomain=$((attemptPerDomain + 1))
done

rm -rf $domain"problem_files_temp/"
rm -rf $domain"problems/"


