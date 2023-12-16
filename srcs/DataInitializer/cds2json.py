import re
import json
import os

def fasta_to_json():
    entries = {}
    extras = []
    with open(fasta_file_path, 'r') as f:
        lines = f.readlines()
    l = len(lines)
    # Iterate through the lines of the FASTA file
    i = 0
    cnt = 0
    entry_cnt=0
    extra_cnt=0
    while i < l:
        # Check if the line is a header line
        if lines[i].startswith('>lcl|'):
            cnt += 1
            match = re.search(r'>lcl\|(.+?) \[gene=(.+?)\] \[locus_tag=(.+?)\] \[db_xref=UniProtKB/Swiss-Prot:(.+?)\] \[protein=(.+?)\] \[protein_id=(.+?)\] \[location=(.+?)\] \[gbkey=CDS\]',lines[i])
            if match: # Normal entry
                entry_cnt += 1
                entry = {'id':match.group(1),
                         'gene':match.group(2),
                         'locus_tag':match.group(3),
                         'UniProtKB_db_xref':match.group(4),
                         'protein':match.group(5),
                         'protein_id':match.group(6),
                         'location':match.group(7),
                         'sequence': ''}
                # Iterate through the sequence lines
                i += 1
                while i < l and not lines[i].startswith('>'):
                    entry['sequence'] += lines[i].strip()
                    i += 1
                entries[match.group(4)] = entry
            else: # Abnormal entry, apart to extras
                extra_cnt += 1
                entry = {}
                m = re.search(r'>lcl\|(.+?) \[gene=(.+?)\] \[locus_tag=(.+?)\] \[db_xref=(.+?)\] \[protein=(.+?)\] \[protein_id=(.+?)\] \[location=(.+?)\] \[gbkey=CDS\]',lines[i])
                n = re.search(r'>lcl\|(.+?) \[gene=(.+?)\] \[locus_tag=(.+?)\] \[db_xref=(.+?)\] \[protein=(.+?)\] \[pseudo=(.+?)\] \[location=(.+?)\] \[gbkey=CDS\]',lines[i])
                if m and not n:
                    entry = {'MEMO':"NO UniProtKB db_xref",
                             'id':m.group(1),
                             'gene':m.group(2),
                             'locus_tag':m.group(3),
                             'db_xref':m.group(4),
                             'protein':m.group(5),
                             'protein_id':m.group(6),
                             'location':m.group(7),
                             'sequence': ''}
                if n and not m:
                    entry = {'MEMO':"NO UniProtKB db_xref and PSEUDO=TRUE",
                             'id':n.group(1),
                             'gene':n.group(2),
                             'locus_tag':n.group(3),
                             'db_xref':n.group(4),
                             'protein':n.group(5),
                             'protein_id':"NONE because PSEUDO=TRUE",
                             'location':n.group(7),
                             'sequence': ''}
                # Iterate through the sequence lines
                i += 1
                while i < l and not lines[i].startswith('>'):
                    entry['sequence'] += lines[i].strip()
                    i += 1
                extras.append(entry)
        else:
            i += 1
    # Convert the list of entries to JSON
    json_data = json.dumps(entries, indent=2)
    extra_data = json.dumps(extras, indent=2)
    # Save JSON to a file (optional)
    with open(json_file_path, 'w') as j:
        j.write(json_data)
    with open(extra_json_file_path, 'w') as j:
        j.write(extra_data)
    print(f"{cnt} entries detected in total, with")
    print(f"{entry_cnt} normal entries saved to {json_file_path} and")
    print(f"{extra_cnt} abnormal entries saved to {extra_json_file_path}")

curr_dir = os.path.curdir # project dir (base dir)
fasta_file_path = os.path.join(curr_dir , "data/OriginData/cds_from_genomic.fna")
json_file_path = os.path.join(curr_dir , "data/JsonData/cds_json.json")
extra_json_file_path = os.path.join(curr_dir , "data/JsonData/aborted_cds_json.json")
fasta_to_json()