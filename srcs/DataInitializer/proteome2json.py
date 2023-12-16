import re
import json
import os

def fasta_to_json(fasta_file, json_file):
    entries = {}
    with open(fasta_file, 'r') as f:
        lines = f.readlines()
    l = len(lines)
    # Iterate through the lines of the FASTA file
    i = 0
    cnt = 0
    while i < l:
        # Check if the line is a header line
        if lines[i].startswith('>sp|'):
            cnt += 1
            match = re.search(r'>sp\|(.+?)\|(.+?)_ECOLI (.+?) (OS=Escherichia coli \(strain K12\) OX=83333) GN=(.+?) PE=([1-5]) SV=([1-7])',lines[i])
            if match: # Normal entry
                entry = {'id':match.group(1),
                         'abbr':match.group(2)+"_ECOLI",
                         'name':match.group(3),
                         'GN':match.group(5),
                         'PE':match.group(6),
                         'SV':match.group(7),
                         'extrainfo':match.group(4),
                         'sequence': ''}
                # Iterate through the sequence lines
                i += 1
                while i < l and not lines[i].startswith('>'):
                    entry['sequence'] += lines[i].strip()
                    i += 1
                entries[match.group(1)] = entry
        else:
            i += 1
    # Convert the list of entries to JSON
    json_data = json.dumps(entries, indent=2)
    # Save JSON to a file (optional)
    with open(json_file, 'w') as j:
        j.write(json_data)
    print(f"{cnt} entries detected in total, saved to {json_file}")

curr_dir = os.path.curdir # project dir (base dir)
# Example usage
fasta_file_path = os.path.join(curr_dir , "data/OriginData/UP000000625_83333.fasta")
json_file_path = os.path.join(curr_dir , "data/JsonData/proteome_json.json")
json_data = fasta_to_json(fasta_file_path, json_file_path)