#!/usr/bin/env bash

#./Scripts/LPG_solve.sh domain.pddl Input/blocksworld/domain/ problem_04_300.pddl Input/blocksworld/instances/ 60s
DOMAIN="$1" # Name of the domain
DOMAINNOEXT="${DOMAIN%.*}"
DOMAINFOLDER="$2"
PROBLEM="$3"
PROBLEMNOEXT="${PROBLEM%.*}"
PROBLEMFOLDER="$4"
TIMEOUT="$5" #Max allowe time
OUTTMPFILE=tmp/LPG/"$DOMAINNOEXT$PROBLEMNOEXT"

mkdir -p tmp/LPG/

#REMOVE OLD COPIES
if [ -f "$OUTTMPFILE.SOL" ] ; then
    rm "$OUTTMPFILE.SOL"
fi;

#timeout "$TIMEOUT" ./Planners/LPG-td-1.4/lpg-td -o $DOMAINFOLDER$DOMAIN -f $PROBLEMFOLDER$PROBLEM -speed -out $OUTTMPFILE > res.tmp
timeout "$TIMEOUT" ./Planners/LPG-td-1.4/lpg-td -o $DOMAINFOLDER$DOMAIN -f $PROBLEMFOLDER$PROBLEM -quality -out $OUTTMPFILE > res.tmp


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