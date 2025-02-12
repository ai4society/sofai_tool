#!/bin/bash
# Script to generate $1 problem files for the domains. These instances should require at least $2 seconds to be solved by the fastet planner we have and within $3 tries. $4 Activate (if == 1) optimality calculation
# Usage from the "Scripts/ProblemGenerator" folder execute "./completeGenerator.sh 150 0.5 1000 1"
# Each instance will be below 512 token and should require more than 0.5 seconds to be solved by LPG. Finally, all domains will try to generate a maximum of 1000 instances and for each one the optiaml plan is calculated

max_tokens=512
outFolder="Output/"
dmnFolder="domain/"
instFolderEasy="instancesEasy/"
instFolderHard="instancesHard/"
instFolderBigEasy="instancesBigEasy/"
instFolderBigHard="instancesBigHard/"
origOptPath="noOpt/"
minimumTime=$2
declare -i maxAttemptsPerDomain=$3
optimality=$4
optimality_time=30

#Blocksworld specific
declare -i maxBlockNum=11
declare -i minBlockNum=10
blocksNum=$minBlockNum
bwFolder="blocksworld/"

#Driverlog specific
dlFolder="driverlog/"

#Ferry specific
ferryFolder="ferry/"

#Gripper specific
grFolder="grippers/"

#Hanoi specific
hanoiFolder="hanoi/"

#Hanoi specific
miconicFolder="miconic/"

#Logistics specific
logisticsFolder="logistics/"

#Rovers specific
roversfolder="rovers/"

#Satellite specific
satellitefolder="satellite/"

#Barman specific
barmanfolder="barman/"


## declare an array variable
#declare -a dmnArr=("$bwFolder")
#declare -a dmnArr=("$hanoiFolder" "$miconicFolder" "$grFolder" "$ferryFolder" "$bwFolder" "$dlFolder" "$logisticsFolder" "$roversfolder" "$satellitefolder" "$barmanfolder")
declare -a dmnArr=("$barmanfolder")

## now loop through the above array
for domain in "${dmnArr[@]}"
do

  echo -e "\nWorking on $domain..."

  if [ "$domain" != "$hanoiFolder" ]; then 
    cd $domain
    make > /dev/null
    cd ..
  fi


  tempDmnFolder=$outFolder$domain$dmnFolder
  tempInstancesDirEasy=$outFolder$domain$instFolderEasy
  tempInstancesDirHard=$outFolder$domain$instFolderHard
  tempInstancesDirBigEasy=$outFolder$domain$instFolderBigEasy
  tempInstancesDirBigHard=$outFolder$domain$instFolderBigHard


  mkdir -p $tempDmnFolder
  mkdir -p $tempInstancesDirEasy$origOptPath
  mkdir -p $tempInstancesDirHard$origOptPath
  mkdir -p $tempInstancesDirBigEasy$origOptPath
  mkdir -p $tempInstancesDirBigHard$origOptPath


  declare -i attemptPerDomain=0
  declare -i counter=0

  while (( $counter < $1 && $attemptPerDomain < $maxAttemptsPerDomain )); do



    if [ "$domain" = "$bwFolder" ]; then 
      #blocksNum only for blocksworld
      result=$(./"$domain"/generator_single.sh "$blocksNum")
      
      blocksNum=$(( blocksNum+1 ))
      if (( $blocksNum > $maxBlockNum )); then
        blocksNum=$minBlockNum
      fi
    else
      result=$(./"$domain"/generator_single.sh)
    fi


    seprated_res=($result)

    domain_file="${seprated_res[0]}"
    problem_file="${seprated_res[1]}"


    if [ -z "$(ls -A $tempDmnFolder)" ]; then
      cp $domain_file $tempDmnFolder/domain.pddl
    fi
    optimal_lenght=-1
    optPath=$origOptPath
    #Optimality checker
    if (( $optimality == 1)); then
      timeout "$optimality_time"s python3 ../../Planners/FastDownward/fast-downward.py --plan-file planopt.tmp $domain_file $problem_file  --search "astar(blind())" > /dev/null
      if [ $? -eq 124 ]; then 
        optimal_lenght=-1
        optPath=$origOptPath
      else
        optimal_lenght=`wc --lines < planopt.tmp`
        optimal_lenght=$((optimal_lenght - 1))
        optPath=""
      fi
    fi
    echo -e "; Optimality lenght is (:optlen $optimal_lenght)\n" | cat - $problem_file > optFileName.tmp && mv optFileName.tmp $problem_file

    #Checking for token limitations
    prompt=$(python plansformer_prompt_generator.py "$domain_file" "$problem_file")
    token_count=$(python count_512subset.py "$prompt")

    #echo "token is $token_count"
    #token_count=100
    
    filename=$(basename -- "$problem_file")
    #Checking for token limitations
    if (( $token_count <= $max_tokens )); then

      #Checking for solving time limitations
      timeout "$minimumTime"s ./../../Planners/LPG-td-1.4/lpg-td -o $domain_file -f $problem_file -speed -out plan.tmp > /dev/null
      if [ $? -eq 124 ]; then #If we take more than the minimum time to solve with LPG fast we add it
        cp $problem_file $tempInstancesDirHard$optPath$filename
        
        if (( $optimal_lenght > 0)); then
          counter=$((counter + 1))
        fi
        
        echo "Added problem" $filename
      else
        cp $problem_file $tempInstancesDirEasy$optPath$filename
        echo "Discarded problem" $filename  "solved too fast by LPG"
      fi
    else
      echo "Discarded problem" $filename  "because has too many tokens"
      timeout "$minimumTime"s ./../../Planners/LPG-td-1.4/lpg-td -o $domain_file -f $problem_file -speed -out plan.tmp > /dev/null
      if [ $? -eq 124 ]; then #If we take more than the minimum time to solve with LPG fast we add it
        cp $problem_file $tempInstancesDirBigHard$optPath$filename
      else
        cp $problem_file $tempInstancesDirBigEasy$optPath$filename
      fi      
    fi 

    attemptPerDomain=$((attemptPerDomain + 1))
    #sleep 1s
  done

  rm -rf $domain"problem_files_temp/"

done

