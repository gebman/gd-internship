# Write a script that gets system information like distro info,
# memory(total, used, free), CPU info (model, core numbers, speed),
# current user, system load average, and IP address. Use arguments for specifying resources.
# (For example, -d for distro -m for memory, -c for CPU, -u for user info,
# -l for load average, -i for IP address).

import argparse
import re
import os


parser = argparse.ArgumentParser(description="Gathers various system information and prints it out. Only works on Linux distros.")

parser.add_argument("-d", "--distro", action="store_true")
parser.add_argument("-m", "--memory", action="store_true")
parser.add_argument("-c", "--cpu", action="store_true")
parser.add_argument("-l", "--load", action="store_true")
parser.add_argument("-i", "--ip", action="store_true")
parser.add_argument("-u", "--user", action="store_true")

args = vars(parser.parse_args())

if not any(args.values()):
    parser.error("provide at least one argument")

if args["distro"]:
    with open("/etc/os-release") as file:
        for line in file.readlines():
            if re.match('NAME="*"', line):
                print(f"Distro name: {line[6:-2]}")

if args["memory"]:
    with open("/proc/meminfo") as file:
        lines = dict([[y.strip() for y in x.split(":")] for x in file])

        print("Total memory:",int(lines["MemTotal"][:-3])/1000,"MB")
        print("Used memory:",(int(lines["MemTotal"][:-3])-int(lines["MemFree"][:-3]))/1000,"MB")
        print("Free memory:",int(lines["MemFree"][:-3])/1000,"MB")


if args["cpu"]:
    with open("/proc/cpuinfo") as file:
        cpu_list = []
        for cpu_raw in file.read().split("\n\n"):
            if cpu_raw == '':
                continue
            cpu = dict()
            for line in cpu_raw.split("\n"):
                record = [x.strip() for x in line.split(":")]
                cpu[record[0]] = record[1]
            cpu_list.append(cpu)

        cpu_names = []
        for i in range(len(cpu_list)):
            if cpu_list[i]["model name"] not in [x[0] for x in cpu_names]:
                cpu_names.append([cpu_list[i]["model name"],int(cpu_list[i]['cpu cores']),int(cpu_list[i]['siblings']),cpu_list[i]['cpu MHz']])
            else:
                for j in range(len(cpu_names)):
                    if cpu_names[j][0] == cpu_list[i]["model name"]:
                        cpu_names[j][1] += int(cpu_list[i]["cpu cores"])
                        cpu_names[j][2] += int(cpu_list[i]["siblings"])
                    
        for x,y in enumerate(cpu_names):
            print(f"CPU {x}:")
            print(f"\tProcessor name: {y[0]}")
            print(f"\tCores: {y[1]}")
            print(f"\tThreads: {y[2]}")
            print(f"\tSpeed: {round(float(y[3]))}MHz")

if args["user"]:
    print(f"Username: {os.environ.get('USER')}")

if args["load"]:
    with open("/proc/loadavg") as file:
        values = file.read().split()
        print("CPU utilization avg in: ")
        print(f"Last 1 min: {float(values[0])*100}%")
        print(f"Last 5 min: {float(values[1])*100}%")
        print(f"Last 10 min: {float(values[2])*100}%")
if args["ip"]:
    #WIP
    pass
