#!/usr/bin/env bash
#This script prints out the time for executing a plan, giventhe actions, on the same domain with the two version of PDKB
#USAGE EXAMPLE (from the project root folder): ". scripts/givenplan_comparison.sh exp/paper/CC/CC_2_2_3.txt right_a left_b a_check_3"
#	where:
#			"exp/paper/CC/CC_2_2_3.txt" is the path to the domain name
#			"right_a left_b a_check_3" are the names of three actions (the number of actions can be any n > 0)
PROBLEM="$1" # Name of the domain
DOMAINFOLDER="$2"
TIMEOUT="$3" #Max allowe time


mkdir -p tmp/PDKB/
touch tmp/PDKB/$PROBLEM


timeout "$TIMEOUT" python3 Planners/PDKB/pdkb/planner.py $DOMAINFOLDER$PROBLEM > tmp/PDKB/$PROBLEM;

if [ $? -eq 124 ]; then
  echo -e "PDKB TIMED-OUT" >> tmp/PDKB/$DOMAIN;
fi;
