#!/usr/bin/env bash
#USAGE EXAMPLE (from the project root folder): "./Scripts/repo_setup.sh"

## Environment Management
mkdir -p Memory

## EFP Management -- make required
#echo -e "\n\n\nPreparing EFP\n\n\n"
#cd Planners/EFP
#make
#cd ../..
#echo -e "\n\n\nDONE Preparing EFP\n\n\n"


## FastDownward Management
echo -e "\n\n\nPreparing FastDownward\n"
cd Planners/FastDownward
python3 build.py
cd ../..
echo -e "\nDONE Preparing FastDownward\n\n\n"


## Plansformers Management
pip install --upgrade --no-cache-dir gdown

echo -e "\n\n\nPreparing Plansformer v1.0\n"
cd Planners/PlansformerS1/model_files
#Plansformer 1.0
gdown "https://drive.google.com/uc?id=1960ZL8-iYBvV3zwYqF1zL8CMhT8ugFPq"
cd ../../..
echo -e "\nDONE Preparing Plansformer v1.0\n\n\n"

sleep 5  # Waits 5 seconds.

echo -e "\n\n\nPreparing Plansformer v2.0\n"
cd Planners/New_PlansformerS1/mode0_model_files
#Plansformer 2.0 -- MODE 0 File
gdown "https://drive.google.com/uc?id=1960ZL8-iYBvV3zwYqF1zL8CMhT8ugFPq"
sleep 5  # Waits 5 seconds.

cd ../mode1_model_files
#Plansformer 2.0 -- MODE 1 File
gdown "https://drive.google.com/uc?id=1d8csJA9tGRNfj3ugktuhtucq4c9vSdPg"
cd ..
mkdir mode2_model_files #Plansformer 2.0 -- MODE 2 Folder
echo -e "\nDONE Preparing Plansformer v2.0\n\n\n"
