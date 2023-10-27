#!/bin/bash
# Write bash script accepting operation parameter (“-”, “+”, “*”, “%”), sequence of numbers and debug flag. For example:
#  ./your_script.sh -o % -n 5 3 -d > Result: 2
# ./your_script.sh -o + -n 3 5 7 -d > Result: 15
# If -d flag is passed, script must print additional information:
# User: <username of the user running the script>
# Script: <script name>        
# Operation: <operation>
# Numbers: <all space-separated numbers>
while getopts "o:n:d" args; do
    case ${args} in
    o)
    operator=$OPTARG ;;
    n)
    numbers=($OPTARG) ;;
    d)
    echo "Username: "$USER
    echo "Script: "$0
    echo "Operation: "$operator
    echo "Numbers: "${numbers[@]}
    esac
done

result=${numbers[0]}
for num in ${numbers[@]:1}; do
    result=$(( ${result} $operator ${num} ))
done
echo "Result: "$result
