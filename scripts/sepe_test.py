import os
from Seperator import Seperator

Read_path= "../resources/Circle"
Output_mainpath="../Circle/sep"
Core="Sn"
Ligand="C"

if __name__=="__main__":
    output_mainpath=Output_mainpath
    if not os.path.exists(output_mainpath):
        os.mkdir(output_mainpath)
    for file in os.listdir(Read_path):
        output_path=output_mainpath+"/"+"{}".format(file.split(".")[0])
        Seperator=Seperator(Read_path + "/" + file, output_path)
        r=Seperator.run(Core,Ligand)
        if r=="No_core_ligand_pair_error":
            print("Trying to use O as the ligand...")
            Seperator=Seperator(Read_path + "/" + file, output_path)
            r=Seperator.run("Sn","O")
            if r=="No_core_ligand_pair_error":
                print("Failed to generate core_ligand_pair for {}.".format(file))