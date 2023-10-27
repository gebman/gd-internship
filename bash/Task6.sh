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
rm -f logfile.txt
date >> logfile.txt
echo "Username: "$USER >> logfile.txt
#TODO internal ip address
echo "Hostname: "`hostname` >> logfile.txt
echo "Public IP address: "`dig TXT +short o-o.myaddr.l.google.com @ns1.google.com` >> logfile.txt
#TODO distro info

IFS=', '
uptime_arr=(`uptime`)
echo "Uptime: "${uptime_arr[2]} >> logfile.txt

df_arr=(`df -g / | sed -n '2 p'`)
echo "Used disk space: "${df_arr[2]}"/"${df_arr[1]}"GB" >> logfile.txt

ram_arr=(`free -h | grep "Mem:"`)
echo "Used, Free, Total RAM:" ${ram_arr[2]} ${ram_arr[3]} ${ram_arr[1]} >> logfile.txt

#TODO CPU info


