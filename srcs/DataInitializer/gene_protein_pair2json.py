import json
import csv
import os

def cds_proteome_checker():
    with open(cds_file_path,'r') as f:
        cds_data = json.load(f)
    with open(proteome_file_path,'r') as f:
        proteome_data = json.load(f)
    cnt = 0

    cds_data:dict
    proteome_data:dict
    entries = {}
    extras = {}

    to_remove=[]

    ori_cds_len = len(cds_data) # original cds entries num
    ori_proteome_len = len(proteome_data) # original proteome entries num
    have_gene_no_protein = 0 # gene missing protein num
    have_protein_no_gene = 0 # protein missing gene num
    gene_protein_oripair = 0 # original gene-protein pair num
    gene_protein_len_err = 0 # lenth error pair num
    gene_protein_seq_err = 0 # sequence error pair num
    perfect_gene_protein = 0 # final perfect pair num

    # check whether have gene but no protein
    for i in cds_data:
        if not proteome_data.get(i):
            have_gene_no_protein += 1
            to_remove.append(i)
            mRNA = cds_data[i].pop("sequence").replace("T","U")
            extras[i]={"MEMO":"NO PROTEIN DATA",
                       "gene_data":cds_data[i],
                       "protein_data": None,
                       "mRNA_sequence":mRNA,
                       "protein_sequence": None}
    for i in to_remove:
        cds_data.pop(i)
    to_remove.clear()

    # check whether have protein but no gene
    for i in proteome_data:
        if not cds_data.get(i):
            have_protein_no_gene += 1
            to_remove.append(i)
            protein = proteome_data[i].pop("sequence")
            extras[i]={"MEMO":"NO CDS DATA",
                       "gene_data": None,
                       "protein_data": proteome_data[i],
                       "mRNA_sequence": None,
                       "protein_sequence": protein}
    for i in to_remove:
        proteome_data.pop(i)
    to_remove.clear()

    # set codons dict
    codons = {}
    with open(codon_csv, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            codons[row[0]]=row[1]
        codons.pop("Codon")

    # load sequences
    for i,j in cds_data.items():
        gene_protein_oripair += 1
        k = proteome_data.get(i)
        mRNA = j.pop("sequence").replace("T","U")
        protein = k.pop("sequence")
        mRNA:str
        protein:str

        # check whether have lenth error
        if len(mRNA)/3-1 != len(protein):
            gene_protein_len_err += 1
            extras[i]={"MEMO":"LENTH ERROR",
                       "gene_data": j,
                       "protein_data": k,
                       "mRNA_sequence": mRNA,
                       "protein_sequence": protein}

        # check whether have sequence error
        else:
            err = False
            for idx in range(len(protein)):
                if codons[mRNA[idx*3 : idx*3+3]] != protein[idx]:
                    err = True
                    break
            if err:
                gene_protein_seq_err += 1
                extras[i]={"MEMO":"SEQUENCE ERROR",
                           "gene_data": j,
                           "protein_data": k,
                           "mRNA_sequence": mRNA,
                           "protein_sequence": protein}

            # WELL DONE and this is a perfect gene-protein pair!
            else:
                perfect_gene_protein += 1
                entries[i]={"gene_data": j,
                            "protein_data": k,
                            "mRNA_sequence": mRNA,
                            "protein_sequence": protein}


    # Convert the list of entries to JSON
    json_data = json.dumps(entries, indent=2)
    extra_data = json.dumps(extras, indent=2)
    # Save JSON to a file (optional)
    with open(json_file_path, 'w') as j:
        j.write(json_data)
    with open(extra_json_file_path, 'w') as j:
        j.write(extra_data)

    print(f"{ori_cds_len} entries detected in cds_json with")
    print(f"{have_gene_no_protein} entries missing protein,")
    print(f"{ori_proteome_len} entries detected in proteome_json with")
    print(f"{have_protein_no_gene} entries missing gene.")
    print("")
    print(f"{gene_protein_oripair} gene-protein pairs gotten with")
    print(f"{gene_protein_len_err} pairs error in length and")
    print(f"{gene_protein_seq_err} pairs error in sequence.")
    print(f"Entries above saved to {extra_json_file_path}, while")
    print(f"{perfect_gene_protein} perfect gene-protein pairs saved to {json_file_path}.")




curr_dir = os.path.curdir # project dir (base dir)
codon_csv = os.path.join(curr_dir , "srcs/Defs/Codon.csv")
cds_file_path = os.path.join(curr_dir , "data/JsonData/cds_json.json")
proteome_file_path = os.path.join(curr_dir , "data/JsonData/proteome_json.json")
json_file_path = os.path.join(curr_dir , "data/JsonData/selected_data_json.json")
extra_json_file_path = os.path.join(curr_dir , "data/JsonData/aborted_data_json.json")
cds_proteome_checker()