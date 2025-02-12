#!/usr/bin/env bash
#USAGE EXAMPLE (from the project root folder): "./Scripts/batch_list_SOFAI.sh Input/FilesList/NewPlansformerInputFile_0.txt SOFAI-PF-FD 1 7 2 201"
#	where:
#			"Input/FilesList/NewPlansformerInputFile_0.txt" is the name of the file containing all the problems (shuffled) to be solved
#     "SOFAI-PF-FD" is the name of the used approach
#     "1" is the type of System-2 -- in this particular case Fastdownward
#     "7" is the type of System-1 -- in this particular case NewPlansformer
#       "1" is the mode in which we are using NewPlansformer (can be 1,2, or 3 for no_continual, continual, and scratch_continual) -- No need to specify if you are not using this argument
#       "201" is the training size if we are using newPlansformer in mode 2 or 3  -- No need to specify if you are not using this argument

instancesfile="$1" # Name of the file containing all the problems
approachName="$2"
system2="$3"
system1="$4"
PF_type=""
training_size=""

if [[ "$system1" == "6" ]] || [[ "$system1" == "7" ]]; then
  PF_type=$5
  if [[ "$PF_type" == "2" ]] || [[ "$PF_type" == "3" ]]; then
    training_size=$6
  fi
fi

FILEMem="Utilities/fresh_classical.json"

mkdir -p tmp/SOL/
touch tmp/SOL/"sol.out"
echo "" > tmp/SOL/"sol.out"

mkdir -p Memory/
if test -f "$FILEMem"; then
  cp -f $FILEMem "Memory/cases_classical.json"
else
  touch "Memory/cases_classical.json"
  echo -e "{\n\"cases\":{\n}\n}" > "Memory/cases_classical.json"
fi

declare -i instance_count=0
while read -r line;
do
  echo -e "Solving the instance \"$line\"";
  #ADDED "PYTHONNOUSERSITE=1" to ensure local packages over system
  echo -n -e "\n</ist>$instance_count</>" >> tmp/SOL/"sol.out" | python3 sofai_cl_pl.py $line $system2 $system1 $PF_type $training_size >> tmp/SOL/"sol.out";
  instance_count=$(( instance_count+1 ))
done < $instancesfile

declare -i c=0
for file in $(find "Output/SOL"/ -type f); do
  c=$(( c+1 ))
done

mkdir -p Output/SOL/
mv tmp/SOL/sol.out "tmp/SOL/$approachName.sol"
#echo "Solution of $approachName batch test" | mutt -s "$approachName solution" -a tmp/SOL/$approachName.sol -- fabianofrancesco.cs@gmail.com
mv "tmp/SOL/$approachName.sol" "Output/SOL/$approachName"_"$c".sol
