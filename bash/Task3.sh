#!/bin/bash
#You need to write a script that prints the numbers from 1 to 100 such that:
# If the number is a multiple of 3, you need to print "Fizz" instead of that number.
# If the number is a multiple of 5, you need to print "Buzz" instead of that number.
# If the number is a multiple of both 3 and 5, you need to print "FizzBuzz" instead of that number.

for iter in {1..100}; do
    if ! (($iter % 15)); then
        echo "FizzBuzz"
    elif ! (($iter % 3)); then
        echo "Fizz"
    elif ! (($iter % 5)); then
        echo "Buzz"
    else
        echo $iter
    fi
done