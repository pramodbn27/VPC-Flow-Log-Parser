import csv
from collections import defaultdict
import sys
import os

# Function to load lookup table from a CSV file
def load_lookup_table(file_path):
    lookup = {}
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (int(row['dstport']), row['protocol'].lower())
            lookup[key] = row['tag']
    return lookup

# Function to parse a flow log line
def parse_flow_log(log_line):
    fields = log_line.strip().split()
    if len(fields) < 14: # assuming version 2 flow logs has atleast 14 fields
        return None
    return {
        'dstport': int(fields[6]),
        'protocol': {6: 'tcp', 17: 'udp', 1: 'icmp'}.get(int(fields[7]), 'unknown')
    }

# Function to process flow logs
def process_flow_logs(flow_log_path, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    
    with open(flow_log_path, 'r') as f:
        for line in f:
            flow = parse_flow_log(line)
            if flow:
                key = (flow['dstport'], flow['protocol'])
                tag = lookup_table.get(key, 'Untagged')
                tag_counts[tag] += 1
                port_protocol_counts[key] += 1
    return tag_counts, port_protocol_counts

# Function to write output to a CSV file
def write_output(tag_counts, port_protocol_counts, output_file):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        writer.writerow(['Tag Counts:'])
        writer.writerow(['Tag', 'Count'])
        for tag, count in tag_counts.items():
            writer.writerow([tag, count])
        
        writer.writerow([])
        
        writer.writerow(['Port/Protocol Combination Counts:'])
        writer.writerow(['Port', 'Protocol', 'Count'])
        for (port, protocol), count in port_protocol_counts.items():
            writer.writerow([port, protocol, count])

# Main function
def main(flow_log_path, lookup_table_path, output_file):
    lookup_table = load_lookup_table(lookup_table_path)
    tag_counts, port_protocol_counts = process_flow_logs(flow_log_path, lookup_table)
    write_output(tag_counts, port_protocol_counts, output_file)

if __name__ == "__main__":
    flow_log_file = "flow_logs.txt"
    lookup_table_file = "lookup_table.csv"
    output_file = "output.csv"
    
    # Check if custom filenames are provided
    if len(sys.argv) == 4:
        flow_log_file = sys.argv[1]
        lookup_table_file = sys.argv[2]
        output_file = sys.argv[3]
    elif len(sys.argv) != 1:
        print("Usage: python flow_log_parser.py [<flow_log_file> <lookup_table_file> <output_file>]")
        print("If no arguments are provided, default filenames will be used.")
        sys.exit(1)
    
    # Check if files exist
    if not os.path.exists(flow_log_file):
        print(f"Error: Flow log file '{flow_log_file}' not found.")
        sys.exit(1)
    if not os.path.exists(lookup_table_file):
        print(f"Error: Lookup table file '{lookup_table_file}' not found.")
        sys.exit(1)
    
    # Call main function and print output
    main(flow_log_file, lookup_table_file, output_file)
    print(f"Processing complete. Results written to {output_file}")