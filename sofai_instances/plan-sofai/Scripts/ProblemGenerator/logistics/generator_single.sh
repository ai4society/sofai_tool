#!/bin/bash

# Script to generate a problem file.
# Usage from the "Scripts/ProblemGenerator" folder execute "./logistics/generator_single.sh" to generate an instance

mainPath="logistics/"
tmpFolder=$mainPath"problem_files_temp/"
# Check if the problem_files folder exists, if not create it
if [ ! -d $tmpFolder ]; then
  mkdir $tmpFolder
fi

# Assuming the domain file is located in the current directory
domain_file=$mainPath"domain.pddl"

# Define the different configurations
declare -a airplanes=(1 2)
declare -a cities=(1 2 3) #(1 2 3 4 5)
declare -a size=(1) #(1 2 3 4)
declare -a packages=(4 5 6 7) #(4 5 6 7 8 9 10 11 12 13 14 15)

#Select a random configuration
airplanesSize=${#airplanes[@]}
airplanesIndex=$(($RANDOM % $airplanesSize))
citiesSize=${#cities[@]}
citiesIndex=$(($RANDOM % $citiesSize))
sizeSize=${#size[@]}
sizeIndex=$(($RANDOM % $sizeSize))
packagesSize=${#packages[@]}
packagesIndex=$(($RANDOM % $packagesSize))

declare -i c=1
for file in $(find $tmpFolder -type f); do
  c=$(( c+1 ))
done

airplanesVal=${airplanes[$airplanesIndex]}
citiesVal=${cities[$citiesIndex]}
sizeVal=${size[$sizeIndex]}
packagesVal=${packages[$packagesIndex]}

problem_file=$tmpFolder"/problem_logistics_$airplanesVal_$citiesVal_$sizeVal_$packagesVal_$c.pddl"
            
output=$(./"$mainPath"logistics -a $airplanesVal -c $citiesVal -s $sizeVal -p $packagesVal -r $c)
echo "$output" > "$problem_file"

#Print out domain and instance name to feed the next script
echo "$domain_file" "$problem_file"