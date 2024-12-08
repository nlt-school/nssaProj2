#!/bin/python3

import scapy.all as scapy
import subprocess

def filter_packets(value):

    pcap = f'Node{value}.pcap'
    filtered = f'Node{value}_filtered.txt'

    subprocess.run(f'touch {filtered}', shell=True)
    
    packets  = scapy.rdpcap(pcap)

    filteredPackets = []
    for packet in packets:
        if packet.haslayer(scapy.ICMP) and packet[scapy.ICMP].type in [0,8]:
            filteredPackets.append(packet)


    with open(filtered, 'w') as file:
        for packet in filteredPackets:
            file.write(packet.summary() + '\n')

def main():
    count = 1
    while count < 5:
        filter_packets(count)
        count += 1

if __name__ == '__main__':
    main()
