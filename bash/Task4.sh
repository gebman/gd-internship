#!/bin/bash
# Write caesar cipher script accepting three parameters -s <shift> -i <input file> -o <output file>

while getopts "s:i:o:" args; do
    case ${args} in
    s)
        shift=$OPTARG ;;
    i)
        infile=$OPTARG ;;
    o)
        outfile=$OPTARG ;;
    esac
done

: > $outfile
touch $outfile
while read -r line; do
    for i in `seq 0 $(( ${#line} - 1 ))`; do
        char=${line:$i:1}
        if [[ $char == ' ' ]]; then
            printf ' ' >> $outfile
        else
            normal_ascii=$(printf "%d" "'$char")
            shifted_ascii=$(( $normal_ascii + $shift ))
            if [[ ( $normal_ascii -ge 97 && $normal_ascii -le 122 ) && ( $shifted_ascii -lt 97 || $shifted_ascii -gt 122 ) ]]; then
                offset=$(( $(( $shifted_ascii - 97 )) % 26 ))
                shifted_ascii=$(( 97 + $offset ))
            elif [[ ( $normal_ascii -ge 65 && $normal_ascii -le 90 ) && ( $shifted_ascii -lt 65 || $shifted_ascii -gt 90 ) ]]; then
                offset=$(( $(( $shifted_ascii - 65 )) % 26 ))
                shifted_ascii=$(( 65 + $offset ))
            fi
            printf "\x$(printf %x $shifted_ascii)" >> $outfile
        fi
    done
    printf "\n" >> $outfile
done <$infile

