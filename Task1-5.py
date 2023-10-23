# Write a script that gets system information like distro info,
# memory(total, used, free), CPU info (model, core numbers, speed),
# current user, system load average, and IP address. Use arguments for specifying resources.
# (For example, -d for distro -m for memory, -c for CPU, -u for user info,
# -l for load average, -i for IP address).

import argparse
import re
import os
import subprocess
import sys


def distro():
    """
    Prints out name of the distro
    """
    with open("/etc/os-release") as file:
        for line in file.readlines():
            if re.match('NAME="*"', line):
                print(f"Distro name: {line[6:-2]}")


def memory():
    """
    Print out system memory info
    """
    with open("/proc/meminfo") as file:
        lines = dict([[y.strip() for y in x.split(":")] for x in file])

        print("Total memory:", int(lines["MemTotal"][:-3]) / 1000, "MB")
        print(
            "Used memory:",
            (int(lines["MemTotal"][:-3]) - int(lines["MemFree"][:-3])) / 1000,
            "MB",
        )
        print("Free memory:", int(lines["MemFree"][:-3]) / 1000, "MB")


def cpu():
    """
    Print out basic CPU info
    """
    with open("/proc/cpuinfo") as file:
        cpu_list = []
        for cpu_raw in file.read().split("\n\n"):
            if cpu_raw == "":
                continue
            cpu = dict()
            for line in cpu_raw.split("\n"):
                record = [x.strip() for x in line.split(":")]
                cpu[record[0]] = record[1]
            cpu_list.append(cpu)

        cpu_names = []
        for cpu in cpu_list:
            if cpu["model name"] not in [x[0] for x in cpu_names]:
                cpu_names.append(
                    [
                        cpu["model name"],
                        int(cpu["cpu cores"]),
                        int(cpu["siblings"]),
                        cpu["cpu MHz"],
                    ]
                )
            else:
                for i, entry in enumerate(cpu_names):
                    if entry[0] == cpu["model name"]:
                        cpu_names[i][1] += int(cpu["cpu cores"])
                        cpu_names[i][2] += int(cpu["siblings"])

        for number, cpu in enumerate(cpu_names):
            print(f"CPU {number}:")
            print(f"\tProcessor name: {cpu[0]}")
            print(f"\tCores: {cpu[1]}")
            print(f"\tThreads: {cpu[2]}")
            print(f"\tSpeed: {round(float(cpu[3]))}MHz")


def username():
    """
    Print out the current username
    """
    print(f"Username: {os.environ.get('USER')}")


def load():
    """
    Print out CPU load avg
    """
    with open("/proc/loadavg") as file:
        values = file.read().split()
        print("CPU utilization avg in: ")
        print(f"Last 1 min: {float(values[0])*100}%")
        print(f"Last 5 min: {float(values[1])*100}%")
        print(f"Last 10 min: {float(values[2])*100}%")


def ip():
    """
    Print out the IP addresses and network info using "ip addr" or "ifconfig". Currently WIP
    """
    try:
        raw = subprocess.run(["ip", "address"], check=True, text=True, capture_output=True)
        skip_flag = False
        for line in raw.stdout.split("\n"):
            # skip the loopback interface
            if re.match("^.:\slo*", line):
                skip_flag = True
            elif not re.match("^\s{4}", line) and line !='':
                skip_flag = False
                print(f"Device{line.split(':')[1]}:")
            if skip_flag or line =='':
                continue

            ip_info = line.strip().split()
            if ip_info[0]=="inet":
                print("\tIPv4", ip_info[1])
            elif ip_info[0]=="inet6":
                print("\tIPv6",ip_info[1])
        return
    except FileNotFoundError:
        pass
    try:
        raw = subprocess.run(["ifconfig"], check=True, text=True, capture_output=True)
        for device in raw.stdout.split("\n\n"):
            if device[:4]=="lo: " or device=='':
                continue

            print(f"Device {device.split(':')[0]}:")
            for line in device.split("\n"):
                ip_info = line.strip().split()
                if ip_info[0]=="inet":
                    netmask = sum(bin(int(x)).count('1') for x in ip_info[3].split('.'))
                    print(f"\tIPv4 {ip_info[1]}/{netmask}")
                elif ip_info[0]=="inet6":
                    print(f"\tIPv6 {ip_info[1]}/{ip_info[3]}")
            
    except Exception as err:
        print("Error: unable to retrieve ip addresses:",err)
        sys.exit(1)


parser = argparse.ArgumentParser(
    description="Gathers various system information and prints it out. Only works on Linux distros."
)

parser.add_argument("-d", "--distro", action="store_true")
parser.add_argument("-m", "--memory", action="store_true")
parser.add_argument("-c", "--cpu", action="store_true")
parser.add_argument("-l", "--load", action="store_true")
parser.add_argument("-u", "--user", action="store_true")
parser.add_argument("-i", "--ip", action="store_true")

args = vars(parser.parse_args())

if not any(args.values()):
    parser.error("provide at least one argument")

if args["distro"]:
    distro()
if args["memory"]:
    memory()
if args["cpu"]:
    cpu()
if args["load"]:
    load()
if args["user"]:
    username()
if args["ip"]:
    ip()
