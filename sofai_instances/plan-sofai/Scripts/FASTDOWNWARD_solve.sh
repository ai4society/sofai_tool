#!/usr/bin/env bash

#This script prints out the time for executing a plan, giventhe actions, on the same domain with the two version of EFP
#USAGE EXAMPLE (from the project root folder): ". scripts/givenplan_comparison.sh exp/paper/CC/CC_2_2_3.txt right_a left_b a_check_3"
#	where:
#			"exp/paper/CC/CC_2_2_3.txt" is the path to the domain name
#			"right_a left_b a_check_3" are the names of three actions (the number of actions can be any n > 0)
DOMAIN="$1" # Name of the domain
DOMAINNOEXT="${DOMAIN%.*}"
DOMAINFOLDER="$2"
PROBLEM="$3"
PROBLEMNOEXT="${PROBLEM%.*}"
PROBLEMFOLDER="$4"
TIMEOUT="$5" #Max allowe time
OUTTMPFILE=tmp/FastDownward/"$DOMAINNOEXT$PROBLEMNOEXT.out"
TMPPLANFILE="planfd.tmp"

mkdir -p tmp/FastDownward/

#REMOVE OLD COPIES
if [ -f $OUTTMPFILE ] ; then
    rm $OUTTMPFILE
fi;

touch $OUTTMPFILE
touch $TMPPLANFILE

#python3 ./fast-downward.py --plan-file plan.out ../../Input/blocksworld/domain/domain.pddl ../../Input/blocksworld/instances/4/problem_4_1.pddl --search "astar(lmcut)" | grep "Search time:" > time.tmp

#timeout "$TIMEOUT" python3 Planners/FastDownward/fast-downward.py --plan-file $TMPPLANFILE $DOMAINFOLDER$DOMAIN $PROBLEMFOLDER$PROBLEM  --search "astar(lmcut)" > res.tmp
timeout "$TIMEOUT" python3 Planners/FastDownward/fast-downward.py --plan-file $TMPPLANFILE $DOMAINFOLDER$DOMAIN $PROBLEMFOLDER$PROBLEM  --search "astar(blind())" > res.tmp

if [ $? -eq 124 ]; then
  echo -e "FASTDOWNWARD TIMED-OUT" >> $OUTTMPFILE
else

  echo -n "Solution = " >> $OUTTMPFILE
  while read line; do
    if [[ "$line" != *";"* ]]; then
        echo -n "$line" | awk '{printf substr($0, 2, length($0) - 2)}' >> $OUTTMPFILE
        echo -n ", " >> $OUTTMPFILE
    fi
  done < $TMPPLANFILE

  echo "" >> $OUTTMPFILE
  grep -w "Search time:" res.tmp >> $OUTTMPFILE

fi;

if [ -f 'res.tmp' ] ; then
    rm res.tmp
fi;
if [ -f $TMPPLANFILE ] ; then
    rm $TMPPLANFILE
fi;
