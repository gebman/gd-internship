# Given an input string, count occurrences of all characters within a string 
# (e.g. pythonnohtyppy -> p:3, y:3, t:2, h:2, o:2, n:2).

from collections import Counter

def task(input_string):
    return Counter(input_string)

# Example usage
print(task("pythonnohtyppy"))
print(task("gd-internship"))

