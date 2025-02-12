#!/usr/bin/env bash

for robots in {2..3}; do
    for rooms in {2..5}; do
		for balls in {3..5}; do
			python script.py $robots $rooms $balls 1
		done
    done
done


