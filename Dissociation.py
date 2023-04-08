import os
import shutil
import argparse
import sys
from Seperator import seperator
from orca_utils.orca_writer import ORCA_INPUT
from orca_utils.bash_generator import bash_g
from orca_utils.utils import calculate_electron_num

#断键并计算解离能

'''
File Structure
|-Dissociation.py
 |--optimized_structures
 |--(Structure_name)
  |--nu.xyz
  |--ng.xyz
  |--ps.xyz
|--workdir
 |--(Structure_name)
  |--ng
     |--1
      |--bond_cutoff.txt
      |--core.xyz
      |--ligand.xyz
      |--electron_num.txt
      |--core_cal
       |--...
      |--ligand_cal
       |--...
     |--2
      |--...
     |--...
  |--nu
   |--...
  |--ps
   |--...
'''

################################  Parser

parser=argparse.ArgumentParser()

parser.add_argument("--p",default="PBS")
parser.add_argument("--c",default="Sn")
parser.add_argument("--l",default="C")
parser.add_argument("--n",default=10)
parser.add_argument("--f",default="./optimized_structures")

args=parser.parse_args()
################################

# def bash_g(path,platform,script_name):
#     if platform=="PBS":
#         order="qsub"
#     else:
#         order="sbatch"
#     bash_text=  f"cd {path}\n" \
#                 f"{order} {script_name}\n"
#     with open(path+"/natzme.sh","w") as f:
#         f.write(bash_text)
#         f.close()
#     return path+"/natzme.sh"


if __name__=="__main__":
    core=args.c
    ligand=args.l
    opt_num=int(args.n)

    if args.p=="PBS":
        submit_script_name="orca.pbs"
        sub_script_path="./orca_utils/orca.pbs"
    elif args.p=="Slurm":
        submit_script_name="orca.slm"
        sub_script_path = "./orca_utils/orca.slm"
    else:
        print("-p platform needed to be \"PBS\" or \"Slurm\"")
        sys.exit()

####check submitted tasks
    submitted=[]
    if not os.path.exists("./submitted.log"):
        f=open("./submitted.log","w",encoding="utf-8")
        f.write("")
        f.close()
    else:
        f=open("./submitted.log","r")
        submitted=[x.strip() for x in f.readlines()]
        f.close()
####checked

    if not os.path.exists("./workdir"):
        os.mkdir("./workdir")
    wk_path="./workdir"

    opts_path=args.f
    sub_num=0
    for str_dir in os.listdir(opts_path):
        if not sub_num<opt_num:
            print(f"Succeeded to submit {sub_num+1} structures' series tasks.Program exit.")
            break
        if str_dir in submitted:
           continue
        sub_num+=1
        wd_created=False
        str_path=opts_path+f"/{str_dir}"
        submitted.append(str_dir)

        try:
            cur_wkpath=wk_path+f"/{str_dir}"
            if not os.path.exists(cur_wkpath):
                os.mkdir(cur_wkpath)
            wd_created=True

            #initial structure calculation
            initial_path=cur_wkpath+f"/initial"
            if not os.path.exists(initial_path):
                os.mkdir(initial_path)
            se_map={"nu":0,"ng":-1,"ps":1}    #state-electronic map
            for state in ["nu","ng","ps"]:
                whole_str_path = str_path + f"/{state}.xyz"
                shutil.copy(whole_str_path, cur_wkpath)
                ini_sec_path=initial_path+f"/{state}"
                if not os.path.exists(ini_sec_path):
                    os.mkdir(ini_sec_path)
                file_path=cur_wkpath+f"/{state}.xyz"
                electron_num=calculate_electron_num(file_path)
                orca_core_input = ORCA_INPUT("!TPSS DEF2-SVP D3BJ SP", file_path,
                                             electron_num, se_map[state], ["% PAL NPROCS 16 END"])
                orca_core_input.write(ini_sec_path + "/input.inp")
                shutil.copy(sub_script_path, ini_sec_path + "/")
                bashc_path = bash_g(ini_sec_path, args.p, submit_script_name)
                os.system(f"bash {bashc_path}")
            print(f"{str_dir}'s Initial structure SPE calculation submitted.")


            #seperated calculation
            calsit_map={"ng":[(-1,0),(0,-1)],  #calculation_set
                        "nu":[(-1,1), (0,0)],
                        "ps":[(1,0),  (0,1)]  }  #For neural one ,we calculte (core-negative,ligand-positive) and (core-neural,ligand-neural)...
            for state in ["nu","ng","ps"]:
                calsit=calsit_map[state]
                state_path=cur_wkpath+f"/{state}"
                if not os.path.exists(state_path):
                    os.mkdir(state_path)
                try:
                    sepe=seperator(whole_str_path,state_path)
                    sepe.run(core,ligand)
                except ValueError:
                    print("出现切断键后依然联通的结构")
                    continue
                #Seperate Complete
                for situation in os.listdir(state_path):
                    sit_path=state_path+f"/{situation}"
                    # corecal_path=sit_path+"/core_cal"
                    # ligandcal_path=sit_path+"/ligand_cal"
                    # if not os.path.exists(corecal_path):
                    #     os.mkdir(corecal_path)
                    # if not os.path.exists(ligandcal_path):
                    #     os.mkdir(ligandcal_path)
                    #Generate essential files for performing SP calculation by ORCA in core_cal and ligand_cal dir
                    with open(sit_path+"/electron_num.txt","r") as ff:
                        ffl=ff.readlines()
                        ff.close()
                    core_en,ligand_en=ffl[0].split(':')[-1],ffl[1].split(":")[-1]
                    for sit in calsit:
                        core_stat,ligand_stat=sit[0],sit[1]
                        sit_sec_path=sit_path+f"/core{core_stat}ligand{ligand_stat}"
                        #考虑封装
                        if not os.path.exists(sit_sec_path):
                            os.mkdir(sit_sec_path)
                        corecal_path=sit_sec_path+"/core_cal"
                        if not os.path.exists(corecal_path):
                            os.mkdir(corecal_path)
                        ligandcal_path=sit_sec_path+"/ligand_cal"
                        if not os.path.exists(ligandcal_path):
                            os.mkdir(ligandcal_path)
                        #core
                        orca_core_input=ORCA_INPUT("!TPSS DEF2-SVP D3BJ SP",sit_path+"/core.xyz",
                                                               core_en,sit[0],["% PAL NPROCS 16 END"])
                        orca_core_input.write(corecal_path+"/input.inp")
                        shutil.copy(sub_script_path,corecal_path+"/")
                        bashc_path=bash_g(corecal_path,args.p,submit_script_name)
                        os.system(f"bash {bashc_path}")
                        #ligand
                        orca_ligand_input=ORCA_INPUT("!TPSS DEF2-SVP D3BJ SP",sit_path+"/ligand.xyz",
                                                                 ligand_en,sit[1],["% PAL NPROCS 16 END"])
                        orca_ligand_input.write(ligandcal_path+"/input.inp")
                        shutil.copy(sub_script_path,ligandcal_path+"/")
                        bashl_path = bash_g(ligandcal_path, args.p, submit_script_name)
                        os.system(f"bash {bashl_path}")
        except:
            sub_num-=1
            submitted.pop()
            if wd_created==True:
                shutil.rmtree(wk_path+f"/{str_dir}")
            print(f"{str_dir} is in wrong.")

        with open("./submitted.log", "w") as f:
            f.write("\n".join(submitted))
            f.close()

        pass