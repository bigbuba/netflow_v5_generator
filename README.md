Netflow v5 Generator

This script generates NetFlow-packets from CSV-file.

Since updating the Flow should not exceed 60 seconds, the offset point is the script launch time minus 60 seconds (60000 milliseconds). For convenience, this parameter is configurable (REPORT_TIME).
The Example.xlsx file contains sample lines for generating WA and WP events. Save the required sheet as CSV and use as a source for the script.

Requerements:
1. Python3:
   apt-get install python3
2. Python Scapy:
   apt-get install python3-scapy
3. root priveleges

Usage:
python3 NetFlowV5_gen.py

  -c IP, --collector-ip IP
                        IP address of Netflow collector
  -p PORT, --collector-port PORT
                        Flow collector UDP-port
  -f FILENAME, --file FILENAME
                        CSV filename for Netflow generation
  -t REPORT_TIME, --report_time REPORT_TIME
                        Flow report time (milisec, default: 30000)
  -d DEBUG, --debug DEBUG
                        Debug level: 0 = silent, 1 = short format, 2 = full
                        format
  -D DELIMITER, --delimiter DELIMITER
                        CSV-file delimiter (default: comma)
  -P PAUSE, --pause PAUSE
                        Pause between sending Netflow packets (milisec,
                        default: 0)


Example:
python3 NetFlowV5_gen.py -c 192.168.10.11 -p 2055 -f /opt/test.csv -t 30000 -d 1 -D ';' -P 1
