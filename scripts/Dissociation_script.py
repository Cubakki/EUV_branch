import os
import shutil

from Seperator import Seperator
from PES_utils.PES_structure_gener import PES_sg
from orca_utils.orca_writer import ORCA_INPUT
from orca_utils.utils import electron_num_reader,PES_pbs_bash

import argparse
import json
'''
*********************
使用ORCA工作，计算解离能
*********************
'''

'''
由于解离能计算需要对解开的两部分分别优化后再计算能量，因此分为两步
-step1 解离并优化
-step2 计算解离后部分的总能量并得到解离能

鉴于两步分开运行，会在主目录下生成一个json文件(DS_data.json),第二步运行会读取此文件以获取必要信息
json文件储存了路径设置和运行相关信息。在第一步运行前，也可以创建并指定这一文件以读取运行配置信息。
'''

################################  Parser
parser=argparse.ArgumentParser()

parser.add_argument("--step",default=0)
parser.add_argument("--r",default="./PAG")
parser.add_argument("--w",default="./resources/PAG")
parser.add_argument("--C1",default="N")
parser.add_argument("--C2",default="O")
parser.add_argument("--h",default=False)

args=parser.parse_args()
################################

#pre_defined args
keyline1=""
block1=""
keyline2="!TPSS D4  DEF2-SVP SP\n"
block2=["% PAL NPROCS 32 END\n","%scf SmearTemp 5000 \nend"]
pbs_script_name="orca.pbs"

if __name__=="__main__":
    #help part
    if not args.h==False:
        print(#"--step The step you want to execute,1 or 2.Step 2 need \"DS_data.json\"file in the same path to this script.\n"
              "--r Path contains structure files needed to be dealed with.\n"
              "--w Path to write results.\n"
              "--C1 ; --C2 core atom and ligand atom.eg:--C1 \"Sn\" --C2 \"C\"\n"
              "--h help")

    if args.step==0:
        print("Please set step 1 or 2.")
        exit("Program exit for no specified step.")

    if args.step==1:
        #Def some args
        count=1
        Seperator_output_mainpath = args.w
        Initial_structure_path = args.r
        C1 = args.C1 #core element
        C2 = args.C2 #ligand element

        # Start Seperating
        print("Start to seperating")
        # Check output directory
        if not os.path.exists(Seperator_output_mainpath):
            os.mkdir(Seperator_output_mainpath)
        #Load structure files
        for file in os.listdir(Initial_structure_path):
            #specify output_path
            output_path = Seperator_output_mainpath + "/" + "{}".format(file.split(".")[0])
            #register Seperator
            Seperator = Seperator(Initial_structure_path + "/" + file, output_path)
            #Seperating
            r = Seperator.run(C1, C2)
            #Deal with the situation the desired bond is not existing.This part can be modified or delected.
            if r == "No_core_ligand_pair_error":
                print("Trying to use O as the ligand...")
                Seperator = Seperator(Initial_structure_path + "/" + file, output_path)
                r = Seperator.run(C1, "O")
                if r == "No_core_ligand_pair_error":
                    print("Failed to generate core_ligand_pair for {}.".format(file))
        #Seperating Finish
        print("\nSeperating Option completed\n")
        '''
            Seperating_option_completed
            Start to generate orca and pbs files to apply optimizing to cores and ligands.
        '''
        print("Start to prepare and submit optimize tasks.")
        #load
        for mole_stru in os.listdir(Seperator_output_mainpath):
            mole_stru_path = Seperator_output_mainpath + f"/{mole_stru}"
            mole_name = mole_stru.split("_")[0]
            for sepe in os.listdir(mole_stru_path):
                sepe_path = mole_stru_path + f"/{sepe}"
                ele_num_list = electron_num_reader(sepe_path + f"/electron_num.txt") #[total_num,core_ele_num,lig_ele_num]
                core_file_path=sepe_path+"/core.xyz"
                ligand_file_path=sepe_path+"/ligand.xyz"
                core_opt_path=sepe_path+"/core_opt"
                ligand_opt_path=sepe_path+"/ligand_opt"
                os.mkdir(core_opt_path)
                os.mkdir(ligand_opt_path)
                for paths in [[core_file_path,core_opt_path],[ligand_file_path,ligand_opt_path]]:
                    orca=ORCA_INPUT(keyline1,paths[0],ele_num_list[1],block1)
                    orca.write(paths[1]+"/input.inp")
                    shutil.copy("../orca_utils/orca.pbs", paths[1])
                    bash_path = PES_pbs_bash(paths[1], pbs_script_name)
                    #os.system(f"bash {bash_path}")
                    count += 1

        #Save program data to DS_data.json xxx


    if args.step==2:
        pass