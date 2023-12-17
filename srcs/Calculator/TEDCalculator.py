import json
import csv
import os
TOTAL_TRNA_ID = 43

def calculator(protein_id:str)->list[float]:
    # load protein data
    with open(data_file_path) as f:
        data = json.load(f)[protein_id]
    data:dict

    # load tRNA csv
    tRNA_uM={}
    with open(tRNA_csv, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[0] == "ID":
                continue
            tRNA_uM[int(row[0])]=row[2]

    # load Codon2tRNA json
    with open(codon2tRNA_json, 'r') as f:
        codon_tRNA = json.load(f)
    codon_tRNA:dict

    k_list = []
    for id in range(len(data["protein_sequence"])):
        codon = data["mRNA_sequence"][id*3 : id*3+3].lower()
        wc_id = codon_tRNA[codon]["WC"]
        wb_id = codon_tRNA[codon]["WB"]
        nc_id = codon_tRNA[codon]["nc"]
        non_id = list(range(1,TOTAL_TRNA_ID+1)) # to modify after
        T_wc = 0
        T_wb = 0
        T_nc = 0
        T_non = 0
        for i in wc_id:
            non_id.remove(i)
            T_wc += float(tRNA_uM[i])
        for i in wb_id:
            non_id.remove(i)
            T_wb += float(tRNA_uM[i])
        for i in nc_id:
            non_id.remove(i)
            T_nc += float(tRNA_uM[i])
        for i in non_id:
            T_non += float(tRNA_uM[i])
        k = (T_wc+0.5884*T_wb+2.6233e-4*T_nc)/(0.0104+0.4556*T_wc+0.6864*T_wb+0.0613*T_nc+0.0171*T_non)
        k_list.append(k)
    return k_list

curr_dir = os.path.curdir # project dir (base dir)
data_file_path = os.path.join(curr_dir , "data/JsonData/selected_data_json.json")
tRNA_csv = os.path.join(curr_dir , "srcs/Defs/tRNA.csv")
codon2tRNA_json = os.path.join(curr_dir , "srcs/Defs/Codon2tRNA.json")