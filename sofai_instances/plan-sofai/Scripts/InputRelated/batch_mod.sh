#!/usr/bin/env bash
#USAGE EXAMPLE (from the project root folder): "./Scripts/batch_test.sh coininthebox"
#	where:
#			"coininthebox" is the name of the folder containing the domain and the instaces to be modified
INPATH="$1" # Name of the domain

echo -e "\nExecution of architecture in all the instances in Input/"$INPATH"/instances\n"

for instance in $(find $INPATH"/instances"/ -type f); do
  echo -e "    Generating new instance from \"$(basename ${instance%%.*})\""
  python3 instance_modfier.py "$instance"
done
