import os
import shutil

from Seperator import seperator
from PES_utils.PES_structure_gener import PES_sg
from orca_utils.orca_writer import ORCA_INPUT

import argparse

'''
*********************
使用ORCA工作，计算势能面(变键长)
*********************
'''

'''
此脚本将读取一(或一系列):
    1、核(core)的xyz文件
    2、配体(ligand)的xyz文件
    3、连接核与配体的键文件，不做后缀名要求，包含键两侧原子的位置信息，信息格式与xyz文件中相同
    ***三者均应由同一结构文件生成，即二者拼合按坐标排列时可以重构为原结构
并生成计算势能面所需的一系列修改过键长的xyz结构文件。
之后，对每一个生成的结构文件在指定目录下执行ORCA任务（PBS）
'''
'''
工作目录概览:
-root
  -orca_utils
    =orca_writer.py
    =orca.pbs
  =PES_script.py
  -xxxxx_CLP
    -Molecule1
      -1    #Seperated file directory
        =bond_cutoff.txt
        =core.xyz
        =ligand.xyz
        =electron_num.txt
        -PES
          =xxxx0p1A.xyz
          =xxxx0p2A.xyz
          ...
          -orca_dir
            -0p1    #orca工作目录
              =input.inp
              =orca.pbs
              =...
            -0p2
            ...        
      -2
    -Molecule2
    -...
'''

#输入参数设定
parser=argparse.ArgumentParser()

parser.add_argument("--w",default="./PAG")
parser.add_argument("--r",default="./resources/PAG")
parser.add_argument("--C1",default="N")
parser.add_argument("--C2",default="O")
parser.add_argument("--h",default=False)

args=parser.parse_args()
#
Seperator_output_mainpath = args.w
Initial_structure_path = args.r

keyline="!TPSS D4  DEF2-SVP SP\n"
block=["% PAL NPROCS 2 END\n","%scf SmearTemp 5000 \nend"]
pbs_script_name="orca.pbs"

def PES_pbs_bash(target_dir,pbs_script_name):
    '''
    Generate a bash to cd into the specific directory and execute the pbs_script to submit a pbs task.
    :param target_dir: eg:"./a/b/c"
    :return:
    '''
    bash_text = f"echo \" in bash-->target_dir:{target_dir}\"\n" \
                f"cd {target_dir}\n" \
                f"qsub {pbs_script_name}\n" \
                f"echo \"已执行:qsub {pbs_script_name}\""
    # print(bash_text)
    b_name = f"pbs_activate.sh"
    b_path = f"{target_dir}/{b_name}"
    f = open(target_dir+"/"+b_name, 'w')
    f.write(bash_text)
    f.close()
    return b_path


if __name__=="__main__":
    if args.h!=False:
        print("--r Path contains structure files needed to be dealed with.\n"
              "--w Path to write results.\n"
              "--C1 ; --C2 core atom and ligand atom.eg:--C1 \"Sn\" --C2 \"C\"\n"
              "--h help")
    count=1
    Seperator_output_mainpath = Seperator_output_mainpath
    Initial_structure_path = Initial_structure_path
    if not os.path.exists(Seperator_output_mainpath):
        os.mkdir(Seperator_output_mainpath)
    for file in os.listdir(Initial_structure_path):
        output_path = Seperator_output_mainpath + "/" + "{}".format(file.split(".")[0])
        Seperator = seperator(Initial_structure_path + "/" + file, output_path)
        C1=args.C1
        C2=args.C2
        r = Seperator.run(C1, C2)
        if r == "No_core_ligand_pair_error":
            print("Trying to use O as the ligand...")
            Seperator = seperator(Initial_structure_path + "/" +file, output_path)
            r = Seperator.run("Sn", "O")
            if r == "No_core_ligand_pair_error":
                print("Failed to generate core_ligand_pair for {}.".format(file))
    print("\nSeperating Option completed\n")
    '''
    Seperating_option_completed
    Start to generator PES files(Varied bond_lenth xyz file).
    '''
    print("Start to generator PES files")
    for mole_stru in os.listdir(Seperator_output_mainpath):
        mole_stru_path=Seperator_output_mainpath+f"/{mole_stru}"
        mole_name=mole_stru.split("_")[0]
        for sepe in os.listdir(mole_stru_path):
            sepe_path=mole_stru_path+f"/{sepe}"
            PES_path=f"{sepe_path}/PES"
            print("Generate PES files:{}".format(mole_name+"_"+sepe))
            psg=PES_sg(f"{sepe_path}/core.xyz",f"{sepe_path}/ligand.xyz",f"{sepe_path}/bond_cutoff.txt",f"{sepe_path}/PES")
            psg.run(first_name=mole_name+"_"+sepe)
            ele_num_path = sepe_path + f"/electron_num.txt"
            ele_num_f=open(ele_num_path,"r")
            ele_num_both=ele_num_f.readlines()
            ele_num=int(ele_num_both[0].split(":")[1])+int(ele_num_both[1].split(":")[1])
            '''
            Deal with pbs_workdir and necessary_files...
            '''
            print("Deal with pbs_workdir and necessary_files:{}".format(mole_name+"_"+sepe))
            orca_dir_path=PES_path+"/orca_dir"
            for stfile in os.listdir(PES_path):
                stfile_path=PES_path+f"/{stfile}"
                if not os.path.exists(orca_dir_path):
                    os.mkdir(orca_dir_path)
                sec_name=stfile.split("_")[2]
                sec_path=orca_dir_path+"/"+sec_name.split(".")[0]
                os.mkdir(sec_path)
                orca = ORCA_INPUT(keyline, stfile_path, ele_num, block)
                orca.write(sec_path+"/"+"input.inp")
                shutil.copy("orca_utils/orca.pbs", sec_path)
                bash_path=PES_pbs_bash(sec_path,pbs_script_name)
                #os.system(f"bash {bash_path}")
                count+=1

    '''
    Finish
    '''
    print("Succeed to submit {} ORCA tasks.".format(count))