# 3. Create a script that reads the access log from a file. 
# The name of the file is provided as an argument. An output of the script should provide the total number of 
# different User Agents and then provide statistics with the number of requests from each of them.
# Use the access.log.5 file as an example.

import sys
import os
if len(sys.argv)<2:
    raise Exception("argument missing! provide 1 argument with a log file")
elif len(sys.argv)>2:
    raise Exception("too many arguments!")

if not os.path.isfile(sys.argv[1]):
    raise Exception("the path provided isn't a file or it doesn't exist")
file = open(sys.argv[1])

stats = dict()
for line in file.readlines():
    usr_agent = line.split('" "')[-1][:-2]
    if usr_agent not in stats.keys():
        stats[usr_agent] = 1
    else:
        stats[usr_agent] +=1
#print data out
for x in sorted(stats, key = stats.get, reverse=True):
    print(x,"count = ",stats[x])
print("Number of unique agents: ", len(stats))

print("Number of total requests: ", sum(stats.values()))
    


