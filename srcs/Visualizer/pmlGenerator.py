from srcs.Calculator.TEDCalculator import calculator
import os
from k2color import normalizer


def pmlGenerator(name:str, k_seq:list[float], NM:str, AM:str):
    lenth = len(k_seq)
    color_seq = normalizer(k_seq, NM, AM)
    pml_dir = os.path.join(scripts_dir , name + ".pml")
    pml = open(pml_dir,"w")
    print(f"load ..\\data\\pdbs\\UP000000625_83333_ECOLI_v4\\AF-{name}-F1-model_v4.pdb.gz",file=pml)
    for i in range(lenth):
        print(f"select resi {i+1}",file=pml)
        print(f"color {color_seq[i]}, sele",file=pml)
    print("select none",file=pml)
    pml.close()

curr_dir = os.path.curdir
scripts_dir = os.path.join(curr_dir , "scripts/")
pmlGenerator("P00561", calculator("P00561"), "Sin", "Side")