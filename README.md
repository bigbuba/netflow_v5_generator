Netflow v5 Generator

This script generates NetFlow-packets from CSV-file.

Since updating the Flow should not exceed 60 seconds, the offset point is the script launch time minus 60 seconds (60000 milliseconds).
The Example.xlsx file contains sample lines for generating WA and WP events. Save the required sheet as CSV and use as a source for the script.

Requerements:
1. Python3:
   apt-get install python3
2. Python Scapy:
   apt-get install python3-scapy
3. root priveleges

Usage:
python3 NetFlowV5_gen.py -c [NetFlow Collector IP address]
                         -p [NetFlow Collector UDP port]
                         -f [CSV filename]
                         -d [Debug level: "0" = silent, "1" = short output, "2" = full output]

Example:
python3 NetFlowV5_gen.py -c 192.168.10.11 -p 2055 -f /opt/test.csv -d 1

