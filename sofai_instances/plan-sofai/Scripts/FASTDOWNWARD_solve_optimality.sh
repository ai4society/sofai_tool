#!/usr/bin/env bash

DOMAIN="$1" # Name of the domain
DOMAINNOEXT="${DOMAIN%.*}"
DOMAINFOLDER="$2"
PROBLEMFOLDER="$3"
TIMEOUT="$4" #Max allowe time
TMPPLANFILE="planfd.tmp"

mkdir -p tmp/FastDownward/


# Iterate over all files in the PROBLEMFOLDER directory
for file in "$PROBLEMFOLDER"*.pddl; do
    # Ensure the file ends with .pddl
    if [[ "$file" == *.pddl ]]; then
        # Extract the filename (basename) and assign it to PROBLEM
        PROBLEM=$(basename "$file")
        PROBLEMNOEXT="${PROBLEM%.*}"
        OUTTMPFILE=tmp/FastDownward/"$DOMAINNOEXT$PROBLEMNOEXT.out"

        echo "Working on instance \"$PROBLEMNOEXT\" of domain \"$DOMAINNOEXT\""


        # REMOVE OLD COPIES
        if [ -f "$OUTTMPFILE" ]; then
            rm "$OUTTMPFILE"
        fi

        touch "$OUTTMPFILE"
        touch "$TMPPLANFILE"

        # Execute the planner
        timeout "$TIMEOUT" python3 Planners/FastDownward/fast-downward.py \
            --plan-file "$TMPPLANFILE" "$DOMAINFOLDER$DOMAIN" "$PROBLEMFOLDER$PROBLEM" \
            --search "astar(blind())" > res.tmp

        # Check if the planner timed out
        if [ $? -eq 124 ]; then
            echo -e "FASTDOWNWARD TIMED-OUT" >> "$OUTTMPFILE"
        else
            # Process the output if not timed out
            echo -n "Solution = " >> "$OUTTMPFILE"
            while read line; do
                if [[ "$line" != *";"* ]]; then
                    echo -n "$line" | awk '{printf substr($0, 2, length($0) - 2)}' >> "$OUTTMPFILE"
                    echo -n ", " >> "$OUTTMPFILE"
                fi
            done < "$TMPPLANFILE"

            echo "" >> "$OUTTMPFILE"
            grep -w "Search time:" res.tmp >> "$OUTTMPFILE"

            # Count and prepend the number of commas if optlen is not present
            if ! grep -q "(:optlen" "$PROBLEMFOLDER$PROBLEM"; then
                FIRST_LINE=$(head -n 1 "$OUTTMPFILE")
                COMMA_COUNT=$(echo "$FIRST_LINE" | grep -o "," | wc -l)
                sed -i "1s/^/;(:optlen $COMMA_COUNT)\n/" "$PROBLEMFOLDER$PROBLEM"
                echo -e "\tOptimal length is \"$COMMA_COUNT\""
            else
                echo -e "\tOptimal length ALREADY FOUND"
            fi
        fi

        # Cleanup temporary files
        [ -f 'res.tmp' ] && rm res.tmp
        [ -f "$TMPPLANFILE" ] && rm "$TMPPLANFILE"
    fi
done
