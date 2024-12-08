#!/bin/python3

import scapy.all as scapy

def filter_packets(value):

    pcap = f'Node{value}.pcap'
    packetid = set()
    packets = scapy.rdpcap(pcap)
    
    count = 0
    for packet in packets:
        count+=1
        if packet.haslayer(scapy.ICMP) and packet[scapy.ICMP].type in [0,8]:
            packetid.add(count)

    return packetid

def locate_and_write_packets(value, packetid):
 
    txtfile = f'Node{value}.txt'
    filtered = f'Node{value}_filtered.txt'
    
    emptycount = 0
    data = []
    packet = []

    with open(txtfile) as file:
        for line in file:
            if line.strip() == "":
                emptycount+=1
                packet.append(line)
                if emptycount == 2:
                    data.append(packet)
                    packet = []
                    emptycount = 0
            else:
                packet.append(line)

    with open(filtered, 'w') as file:
        for packet in data:
            packet_number = int(packet[1].strip().split()[0])
            if packet_number in packetid:
                for line in packet:
                    file.write(line)
def main():
    count = 1
    while count < 5:
        packetid = filter_packets(count)
        locate_and_write_packets(count, packetid)
        count += 1

if __name__ == '__main__':
    main()
