#!/bin/bash

usage() { echo "Usage: [-n from] [-m to] [-f FILENAME]" >&2; exit 1; }
M='$'
nflag=true
fFlag=true


while getopts n:m:f: option
do
 case "${option}"
 in
 n) nflag=false; N=${OPTARG};;
 m) M=${OPTARG};;
 f) fFlag=false; FILE=${OPTARG};;
 *) usage;;
 esac
done

## Need to put in one conditional
if [ "$nflag" = "true" ]; then
    usage;
fi

if [ "$fFlag" = "true" ]; then
    usage;
fi


# Extract block to check
sed -n $N','$M'p' $FILE > __TMP_FILE__

# check that block
aspell -c __TMP_FILE__

# If there were something to update
if [ -e __TMP_FILE__.bak ]; then
    # Replace the block
    sed -i $N','$M'd' $FILE

    if [ "$M" == "$" ]; then
        cat __TMP_FILE__ >> $FILE
    else
        sed -i $N" e cat __TMP_FILE__" $FILE
    fi

    # Delete extras
    rm __TMP_FILE__.bak
fi

rm __TMP_FILE__

