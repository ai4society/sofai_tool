#!/usr/bin/env bash
#USAGE EXAMPLE (from the project root folder): "./Scripts/batch_test.sh coininthebox"
#	where:
#			"coininthebox" is the name of the folder containing the domain and the instaces to be solved
INPATH="$1" # Name of the domain
mkdir -p tmp/SOL/
mkdir -p Output/SOL/


echo -e "\nExecution of architecture in all the instances in Input/"$INPATH"/instances\n"
for context in $(find "Input/contexts"/ -type f); do
  for threshold in $(find "Input/thresholds"/ -type f); do
    for domain in $(find "Input/"$INPATH"/domain"/ -type f); do

      declare -i d=0
      for file in $(find "tmp/SOL"/ -type f); do
        d=$(( c+1 ))
      done

      SOLNAMETMP=sol_"$(basename ${domain%%.*})"_"$(basename ${context%%.*})"_"$(basename ${threshold%%.*})"_"$d".tmp
      touch tmp/SOL/$SOLNAMETMP
      echo "" > tmp/SOL/$SOLNAMETMP

      for instance in $(find "Input/"$INPATH"/instances"/ -type f); do
        echo -e "    Solving the instance \"$(basename ${instance%%.*})\" with context \"$(basename ${context%%.*})\" and thresholds \"$(basename ${threshold%%.*})\"";
        python3 architecture.py "$domain" "$instance" "$context" "$threshold" "-d" 2 >> tmp/SOL/$SOLNAMETMP;
        #  echo -e "" >> tmp/SOL/"sol.out";
      done

    done

    declare -i c=0
    for file in $(find "Output/SOL"/ -type f); do
      c=$(( c+1 ))
    done

    SOLNAMEOUT=sol_"$(basename ${domain%%.*})"_"$(basename ${context%%.*})"_"$(basename ${threshold%%.*})"_"$c".out
    cp tmp/SOL/$SOLNAMETMP Output/SOL/$SOLNAMEOUT

  done
done
