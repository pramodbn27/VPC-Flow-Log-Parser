# VPC Flow Log Parser

This program parses AWS VPC flow log data and maps each row to a tag based on a lookup table. It then generates an output file containing the count of matches for each tag and the count of matches for each port/protocol combination.

## Requirements

- Python 3.6 or higher
- No additional libraries required

## Usage

1. Assuming that `flow_log_parser.py`, `flow_logs.txt`, and `lookup_table.csv` are in the same directory.

   ```
   python flow_log_parser.py
   ```
   This will use `flow_logs.txt` as the input flow log file, `lookup_table.csv` as the lookup table, and generate `output.csv` as the output file.

2. Specifying custom filenames.

   ```
   python flow_log_parser.py <flow_log_file> <lookup_table_file> <output_file>
   ```
   For example:
   ```
   python flow_log_parser.py /path/my_flow_logs.txt /path/my_lookup_table.csv /path/my_output.csv
   ```

## Input Files

1. Flow Log File: A plain text (ASCII) file containing AWS VPC flow log data.
2. Lookup Table File: A CSV file with the following columns: dstport, protocol, tag.

## Output File

The program generates a CSV file containing:

1. Count of matches for each tag
2. Count of matches for each port/protocol combination

## Assumptions and Limitations

1. The program supports only the default log format (version 2) of AWS VPC flow logs.
2. Input Files: Flow Log File is a plain text (ASCII) file and Lookup Table File is a csv file.
3. Considered the Flow Logs data and Lookup Table data from the sample given in the email.
4. The program follows the AWS documentation and considered 7th field as destination port (dstport) and 8th field as protocol from the Flow Log File.
5. The program only considers the destination port (dstport) and protocol for tag mapping.
6. Protocols are identified as "[6: 'tcp', 17: 'udp', 1: 'icmp]"
7. The flow log file size can be up to 10 MB.
8. The lookup file can have up to 10,000 mappings.
9. Tags can map to more than one port/protocol combination.
10. Matches are case-insensitive.
11. The program assumes that the flow log file and lookup table file are well-formed and contain valid data.
12. The program uses a simple in-memory processing approach, which may not be suitable for extremely large files.

## Testing

- The program has been tested with the sample flow logs and lookup table provided in the email.
- Edge cases such as empty files, files with invalid data, and case sensitivity.
- Here is the output file (output.csv) as the result of running the program with the provided sample data.


## Potential Improvements

1. Add input validation and error handling for malformed input files.
2. Add support for custom log formats and different flow log versions.
3. Optimize memory usage for processing very large files (e.g., using generators or chunked reading).
4. Implement unit tests for individual functions.
5. Add command-line options for verbose output or debug logging.