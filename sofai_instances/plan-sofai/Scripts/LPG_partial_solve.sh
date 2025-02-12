#!/usr/bin/env bash

#./Scripts/LPG_partial_solve.sh domain.pddl Input/blocksworld/domain/ problem_04_300.pddl Input/blocksworld/instances/ s1Sol.tmp 60s
DOMAIN="$1" # Name of the domain
DOMAINNOEXT="${DOMAIN%.*}"
DOMAINFOLDER="$2"
PROBLEM="$3"
PROBLEMNOEXT="${PROBLEM%.*}"
PROBLEMFOLDER="$4"
PARTIALPLANFILE="$5"
TIMEOUT="$6" #Max allowed time
OUTTMPFILE=tmp/LPG/"$DOMAINNOEXT$PROBLEMNOEXT"

mkdir -p tmp/LPG/

#REMOVE OLD COPIES
if [ -f "$OUTTMPFILE.SOL" ] ; then
    rm "$OUTTMPFILE.SOL"
fi;

#timeout "$TIMEOUT" ./Planners/LPG-td-1.4/lpg -o $DOMAINFOLDER$DOMAIN -f $PROBLEMFOLDER$PROBLEM -speed -out $OUTTMPFILE -input_plan $PARTIALPLANFILE > res.tmp
timeout "$TIMEOUT" ./Planners/LPG-td-1.4/lpg -o $DOMAINFOLDER$DOMAIN -f $PROBLEMFOLDER$PROBLEM -quality -out $OUTTMPFILE -input_plan $PARTIALPLANFILE > res.tmp

if [ $? -eq 124 ]; then
  echo -e "LPG TIMED-OUT" >> "$OUTTMPFILE.SOL"
else

  echo "" >> "$OUTTMPFILE.SOL"
  grep -w "Search time:" res.tmp >> "$OUTTMPFILE.SOL"

fi;

if [ -f 'res.tmp' ] ; then
    rm res.tmp
fi;
if [ -f $OUTTMPFILE ] ; then
    rm $OUTTMPFILE
fi;
