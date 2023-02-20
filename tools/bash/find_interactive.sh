#!/bin/bash


BASE_URL="https://s3.amazonaws.com/he-assets-prod/interactives/"
ITERACTIVE="$1"
# 210_comparing_WACC/Launch.html"

END="/Launch.html"

for ((i = 0 ; i <= 100 ; i++)); do
    temp_url=$(printf "%s%.3d_%s%s" "${BASE_URL}" "${i}" "${ITERACTIVE}" "${END}")
    
#     temp_url="${BASE_URL}${i}_${ITERACTIVE}${END}"
#     echo $temp_url
    code=$(curl -Is  "${temp_url}" | grep HTTP | cut -d ' ' -f2)

    if ! [[ "${code}" =~ ^[0-9]+$ ]]; then
        echo "Sorry integers only"
        echo "${temp_url}"
        echo "${code}"
    elif [ "${code}" -eq 200 ]; then
        echo "${temp_url}"
        break
    fi
done 
