# 3. Create a script that reads the access log from a file.
# The name of the file is provided as an argument. An output of the script should provide the total number of
# different User Agents and then provide statistics with the number of requests from each of them.
# Use the access.log.5 file as an example.

import sys
import argparse
from collections import Counter

parser = argparse.ArgumentParser(
    description="this script provides user agent statictics from a log file"
)
parser.add_argument("filename", help="the log file to read")
args = parser.parse_args()

try:
    with open(args.filename, encoding="UTF-8") as file:
        lines = [x.split('" "')[-1][:-2] for x in file.readlines()]
        stats = Counter(lines)

        # Comment out to print all of the sorted statistics
        # for x in sorted(stats, key=stats.get,reverse=True):
        #     print(x, "count: ",stats[x])

        print("Number of unique agents: ", len(stats))
        print("Number of total requests: ", sum(stats.values()))
except OSError as err:
    print("Error: ", err)
    sys.exit(2)
