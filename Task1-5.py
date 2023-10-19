# Write a script that gets system information like distro info,
# memory(total, used, free), CPU info (model, core numbers, speed),
# current user, system load average, and IP address. Use arguments for specifying resources.
# (For example, -d for distro -m for memory, -c for CPU, -u for user info,
# -l for load average, -i for IP address).

import argparse
import sys
import re
import subprocess

parser = argparse.ArgumentParser(description="Gathers various system information and prints it out. Only works on Linux distros.")

parser.add_argument("-d", "--distro", action="store_true")
parser.add_argument("-m", "--memory", action="store_true")
parser.add_argument("-c", "--cpu", action="store_true")
parser.add_argument("-l", "--load", action="store_true")
parser.add_argument("-i", "--ip", action="store_true")
parser.add_argument("-u", "--user", action="store_true")

args = vars(parser.parse_args())

if True not in args.values():
    print("Error: provide at least one argument")
    sys.exit(1)

if args["distro"]:
    with open("/etc/os-release") as file:
        for line in file.readlines():
            if re.match('NAME="*"', line):
                print("Distro name:",line[5:])

if args["memory"]:
    with open("/proc/meminfo") as file:
        lines = dict([[y.strip() for y in x.split(":")] for x in file])

        print("Total memory:",int(lines["MemTotal"][:-3])/1000,"MB")
        print("Used memory:",(int(lines["MemTotal"][:-3])-int(lines["MemFree"][:-3]))/1000,"MB")
        print("Free memory:",int(lines["MemFree"][:-3])/1000,"MB")


if args["cpu"]:
    print("WIP")
    # lines = subprocess.run("lscpu", stdout=subprocess.PIPE)
    # lines = [[y.strip() for y in x.split(":")] for x in lines.stdout.decode().split("\n")]
    # print(lines) 