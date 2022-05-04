#!/bin/bash

## LEO CADA CONFIGURACIÓN Y LA GUARDO EN UN ARRAY
arr=()

file="config_2.txt"

if [[ -f "$file" ]]
then
    i=0 n=0 # salto el header
    while read -r line
        do
            if [[ $n>=$i ]]
                then
                    arr+=("$line")
            fi
            ((n++))

    done < "$file"
else
    echo "$file not found!"  
fi

## OBTENGO NÚMERO DE CONFIGURACIONES GUARDADAS
N=${#arr[@]}

## SETEO CORES Y SUBARRAYS
#arr=("0 1 2 3 4" "0 5 6 7 8" "0 9 10 11 12" "0 13 14 15 16" "0 17 18 19 20")
#N=${#arr[@]}
C=8

C1=()
C2=()
C3=()
C4=()
C5=()
C6=()
C7=()
C8=()

## NÚMERO DE ELEMENTOS POR ARRAY
let r=$N/$C 
let resto=$N%$C

C1=("${arr[@]:0:$r}")
C2=("${arr[@]:$r:2*$r}")
C3=("${arr[@]:2*$r:3*$r}")
C4=("${arr[@]:3*$r:4*$r}")
C5=("${arr[@]:4*$r:5*$r}")
C6=("${arr[@]:5*$r:6*$r}")
C7=("${arr[@]:6*$r:7*$r}")
C8=("${arr[@]:7*$r:8*$r+$resto}")

#echo ${C1[@]} ${#C1[@]} $N "srv1-4.sh"
#echo ${C2[@]} ${#C2[@]} $N "srv1-4.sh"

bash main.sh "${C1[@]}" & bash main.sh "${C2[@]}" & bash main.sh "${C3[@]}" & bash main.sh "${C4[@]}" & bash main.sh "${C5[@]}" & bash main.sh "${C6[@]}" & bash main.sh "${C7[@]}" & bash main.sh "${C8[@]}"

## IMPRIMO EL CONTENIDO DEL ARRAY
#for t in "${arr[@]}"
#do
#echo $t
#done
#echo "Contenido del archivo en el ARRAY"
#echo $N

# ¿cómo marco estados de las corridas? por si hay un corte?

