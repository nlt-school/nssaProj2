#!/usr/bin/python3

# Nolan Trapp 12/8/2024
# NSSA 220 Proh 2 Packet Filtering


import csv

def parse_and_write_to_csv(input_file, output_file):

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)



        writer.writerow(['No.', 'Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info'])
        

        for line in infile:
            if line.strip() and not line.startswith("0000") and line.startswith(" "):  
                parts = line.split()
                packet_no = parts[0]
                time = parts[1]
                source = parts[2]
                destination = parts[3]
                protocol = parts[4]
                length = parts[5]
                info = " ".join(parts[6:])
                


                writer.writerow([packet_no, time, source, destination, protocol, length, info])


def main():
    print("Parsing and writing to CSV files...")
    parse_and_write_to_csv('Node1_filtered.txt', 'parsed/Node1_parsed.csv')
    parse_and_write_to_csv('Node2_filtered.txt', 'parsed/Node2_parsed.csv')
    parse_and_write_to_csv('Node3_filtered.txt', 'parsed/Node3_parsed.csv')
    parse_and_write_to_csv('Node4_filtered.txt', 'parsed/Node4_parsed.csv')
    
    print ("Done! :0")

if __name__ == '__main__':
    main()