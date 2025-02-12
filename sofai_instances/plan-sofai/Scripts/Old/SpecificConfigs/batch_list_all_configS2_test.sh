#!/usr/bin/env bash
# USAGE EXAMPLE (from the project root folder): "./Scripts/batch_list_all_configS2_test.sh Input/FilesList/NewPlansformerInputFile_0.txt"
# Where Input/FilesList/NewPlansformerInputFile_0.txt contains the list of the instances for the tes


instancesfile="$1"


#!/usr/bin/env bash

#cmds=("./Scripts/batch_list_FD.sh $instancesfile" "./Scripts/batch_list_LPG.sh $instancesfile" "./Scripts/batch_list_SOFAI-PF-FD.sh $instancesfile" "./Scripts/batch_list_SOFAI-PF-LPG.sh $instancesfile" "./Scripts/batch_list_SOFAI-PF-FDxLPG.sh $instancesfile" "./Scripts/batch_list_SOFAI-PF-LPGxLPG.sh $instancesfile")

cmds=("./Scripts/batch_list_SOFAI-PF-FD.sh $instancesfile" "./Scripts/batch_list_SOFAI-PF-LPG.sh $instancesfile" "./Scripts/batch_list_SOFAI-PF-FDxLPG.sh $instancesfile" "./Scripts/batch_list_SOFAI-PF-LPGxLPG.sh $instancesfile")

declare -i count=0
mkdir -p S1SOl_Memory
mkdir -p TotSOl_Memory

FILEMem="Utilities/fresh_classical.json"
mkdir -p tmp/SOL/
mkdir -p Output/SOL/

for cmd in "${cmds[@]}"; do
    
    echo -e "\nCleaning repository for new execution"
    
    rm -rf Memory/*
    rm -rf tmp/

    if test -f "$FILEMem"; then
      cp -f $FILEMem "Memory/cases_classical.json"
    else
      touch "Memory/cases_classical.json"
      echo -e "{\n\"size_limit\": 1000,\n\"cases\":{\n}\n}" > "Memory/cases_classical.json"
    fi
    
    echo -e "Running the script: $cmd\n"
    $cmd
    echo -e "\nEnd of the script the script: $cmd"
    
    if [ -e Memory/allS1_solutions.json ]
        then cp Memory/allS1_solutions.json S1SOl_Memory/allS1_solutions_$count.json
    fi
    
    if [ -e Memory/cases_classical.json ]
        then cp Memory/cases_classical.json TotSOl_Memory/cases_classical_$count.json
    fi
    
    count=$((count+1))
    
    sleep 10s
    
done
