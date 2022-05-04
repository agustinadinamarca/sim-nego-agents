#!/bin/bash

chunck=("$@")

#echo "${chunck1[@]}" "${#chunck1[@]}" "ex.sh"

for VARIABLE in "${chunck[@]}"
do
	#echo "$VARIABLE" "ex.sh"
	python3 module/main.py "$VARIABLE"
done

