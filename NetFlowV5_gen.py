#!/usr/bin/python3

import argparse
import datetime
import signal
import time
import csv
import sys

import scapy
from scapy.all import *

send_pause_ms=1
flow_report_time=60000

def main():
    parser = argparse.ArgumentParser(description='Netflow v5 trafic generator')
    parser.add_argument('-c', '--collector-ip', dest='ip',
                        help='IP address of Netflow collector')
    parser.add_argument('-p', '--collector-port', dest='port',
                        help='Flow collector UDP-port')
    parser.add_argument('-f', '--file', dest='filename',
                        help='CSV filename for Netflow generation')
    parser.add_argument('-d', '--debug', dest='debug',
                        help='Debug level: 0 = silent, 1 = short format, 2 = full format')
    args = parser.parse_args()

    if args.ip:
        COLLECTOR_IP = args.ip
    else:
        sys.exit("Collector IP address required")

    if args.port:
        COLLECTOR_PORT = int(args.port)
    else:
        sys.exit("Collector UDP-port required")

    if args.filename:
        CSV_FNAME = args.filename
    else:
        sys.exit("CSV filename required")

    if args.debug:
        DEBUG_LVL = int(args.debug)
    else:
        DEBUG_LVL = 0

    count = 0
    midnight = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    start_flow=(int((datetime.utcnow() - midnight).total_seconds()*1000) - flow_report_time)

    with open(CSV_FNAME) as f:
        reader = csv.reader(f,delimiter=',')
        next(reader) # skip header
        for row in reader:
            if row:
                now_utc = datetime.utcnow()
                uptime_sec = int((now_utc - midnight).total_seconds()) * 1000
                now_sec = int((now_utc - datetime(1970, 1, 1)).total_seconds())

                nfhdr = NetflowHeaderV5(count=1, unixSecs=now_sec, sysUptime = uptime_sec, flowSequence = count )

                nfrec = NetflowRecordV5 (prot=row[0],
                                         src=row[1], srcport=int(row[2]),src_mask=int(row[3]),
                                         dst=row[4], dstport=int(row[5]),dst_mask=int(row[6]),
                                         dpkts=int(row[8]),dOctets=int(row[9]),tcpFlags=int(row[7]),
                                         first=start_flow + int(row[10]),
                                         last= start_flow + int(row[11]))

                netflow = NetflowHeader(version=5) / nfhdr / nfrec

                pkt = Ether() / IP(dst=COLLECTOR_IP, proto='udp') / UDP(dport=int(COLLECTOR_PORT)) / netflow
                if (DEBUG_LVL == 2):
                    pkt.show()
                if (DEBUG_LVL == 1):
                    print ("Flow " + str(count + 1) +": " + str(row[1]) + ":" + str(row[2]) + " -> " + 
                           str(row[4]) + ":" + str(row[5]) + " (" + str(row[9]) + " bytes in " +
                           str(row[8]) + " packets)")
                sendp(pkt, verbose=False)
                time.sleep(send_pause_ms / 1000)
                count = count + 1

    print("Sended flows: " + str(count))

if __name__ == '__main__':
    main()
