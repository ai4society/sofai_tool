#!/usr/bin/env bash
#USAGE EXAMPLE (from the project root folder): "./Scripts/batch_test.sh coininthebox"
#	where:
#			"coininthebox" is the name of the folder containing the domain and the instaces to be solved
# Moreover the fles check if each instance is in "list.tmp" before solving it
INPATH="$1" # Name of the domain

mkdir -p tmp/SOL/
touch tmp/SOL/"sol.out"
echo "" > tmp/SOL/"sol.out"

echo -e "\nExecution of architecture in all the instances in Input/"$INPATH"/instances\n"

for context in $(find "Input/contexts"/ -type f); do
  for threshold in $(find "Input/thresholds"/ -type f); do
    for domain in $(find "Input/"$INPATH"/domain"/ -type f); do
      for instance in $(find "Input/"$INPATH"/instances"/ -type f); do

        while read -r line;
        do
          if [ $instance ==  $line ]; then
          echo -e "    Solving the instance \"$(basename ${instance%%.*})\" with context \"$(basename ${context%%.*})\" and thresholds \"$(basename ${threshold%%.*})\"";
          python3 architecture.py "$domain" "$instance" "$context" "$threshold" "-d" 2 "P2" >> tmp/SOL/"sol.out";
        fi
        #  echo -e "" >> tmp/SOL/"sol.out";
      done < list.tmp
      done
    done
      declare -i c=0
      for file in $(find "Output/SOL"/ -type f); do
        c=$(( c+1 ))
      done

      mkdir -p Output/SOL/
      mv tmp/SOL/"sol.out" Output/SOL/sol_"$(basename ${domain%%.*})"_"$(basename ${context%%.*})"_"$(basename ${threshold%%.*})"_"$c".out
  done
done
