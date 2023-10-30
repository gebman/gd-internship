#!/bin/bash
# Create script, that generates report file with following information:
#  - current date and time;
# name of current user;
# internal IP address and hostname;
# external IP address;
# name and version of Linux distribution;
# system uptime;
# information about used and free space in / in GB;
# information about total and free RAM;
# number and frequency of CPU cores

#only works on linux(partially on mac)
#requires the dig command (sudo yum install bind-utils || sudo apt install dnsutils)
: > logfile.txt
date >> logfile.txt
echo "Username: "$USER >> logfile.txt
echo "Local IP address(es): " `hostname -I` >> logfile.txt
echo "Hostname: "`hostname` >> logfile.txt
echo "Public IP address: "`dig TXT +short +time=5 o-o.myaddr.l.google.com @ns1.google.com` >> logfile.txt
distro=(`hostnamectl | grep "Operating System"`)
echo "Distro: " ${distro[@]:2} >> logfile.txt
IFS=', '
uptime_arr=(`uptime`)
echo "Uptime: "${uptime_arr[2]} >> logfile.txt

df_arr=(`df -h / | sed -n '2 p'`)
echo "Used disk space: "${df_arr[2]}"/"${df_arr[1]} >> logfile.txt

ram_arr=(`free -h | grep "Mem:"`)
echo "Used, Free, Total RAM:" ${ram_arr[2]} ${ram_arr[3]} ${ram_arr[1]} >> logfile.txt

IFS=' '
cpu_model=(`lscpu | grep "Model name"`)
cpu_cores=(`lscpu | grep "Core(s)"`)
cpu_threads=(`lscpu | grep "Thread(s)"`)
cpu_mhz=(`lscpu | grep "BogoMIPS"`)

echo "CPU info:" >> logfile.txt
echo "  Model: " ${cpu_model[@]:2} >> logfile.txt
echo "  Cores: " ${cpu_cores[3]} >> logfile.txt
echo "  Threads: " $(( ${cpu_cores[3]} * ${cpu_threads[3]} )) >> logfile.txt
echo "  Frequency: " ${cpu_mhz[1]} "MHz">> logfile.txt


