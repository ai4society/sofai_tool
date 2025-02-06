#!/usr/bin/env bash
#This script prints out the time for executing a plan, giventhe actions, on the same domain with the two version of EFP
#USAGE EXAMPLE (from the project root folder): ". scripts/givenplan_comparison.sh exp/paper/CC/CC_2_2_3.txt right_a left_b a_check_3"
#	where:
#			"exp/paper/CC/CC_2_2_3.txt" is the path to the domain name
#			"right_a left_b a_check_3" are the names of three actions (the number of actions can be any n > 0)
DOMAIN="$1" # Name of the domain
DOMAINFOLDER="$2"
TIMEOUT="$3" #Max allowe time


mkdir -p tmp/EFP/


#REMOVE OLD COPIES
if [ -f tmp/EFP/$DOMAIN ] ; then
    rm tmp/EFP/$DOMAIN
fi;

touch tmp/EFP/$DOMAIN


timeout "$TIMEOUT" Planners/EFP/bin/efp.out $DOMAINFOLDER$DOMAIN -st "POSS" -check_visited -results_file > res.tmp;

if [ $? -eq 124 ]; then
  echo -e "EFP TIMED-OUT" >> tmp/EFP/$DOMAIN;
else
  grep -w "Solution = " res.tmp >> tmp/EFP/$DOMAIN
fi;


rm res.tmp;
