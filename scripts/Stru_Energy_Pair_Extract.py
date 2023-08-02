#This file is aimed to extract structure file(.xyz) and corresponding single point energy in ORCA's work directory.
import argparse
import os
import copy
import shutil
import json
import csv
'''
-o output dir ,associate as:
        --output dir
            --Stru_E_Pair.txt
            --structures
                --a.xyz
                --b.xyz
                --...
File Stru_E_Pair will be inherit if it is existed


-i input dir(work dir) Program will detect through the dir (and dirs in this dir...)

-r Note that the structure file's name will be renamed by its path information if you not order -r to be False

'''

Stru_E_Pair_Dict={}

def travel_(current_path,function_to_futher_deal_with_files_in_currentdir):
    '''
    思路是只进入文件夹(递归),文件夹内文件的判断处理交给其他函数
    也即此函数作用为：1、列出当前目录下的文件(夹)列表，若有文件夹则递归进入 2、将目前的路径提供给其它函数进一步处理
    :return:
    '''
    fn=function_to_futher_deal_with_files_in_currentdir
    contents=os.listdir(current_path)
    #1
    for sub_entry in contents:
        if os.path.isdir(os.path.join(current_path,sub_entry)):
            travel_(os.path.join(current_path,sub_entry),fn)
        continue
    #2
    function_to_futher_deal_with_files_in_currentdir(current_path)
    pass

def judge_and_deal(current_path : str):
    #只考虑了结构存在于.inp中的情况 ***需要四个global变量
    current_path=current_path.replace("\\","/")
    contents = os.listdir(current_path)
    is_slurm=False
    is_inp=False
    inp_=None
    slurm_=None
    for sub_entry in contents:
        if ".inp" in sub_entry:
            is_inp=True
            inp_path=os.path.join(current_path,sub_entry)
        elif "slurm-" in sub_entry:
            is_slurm=True
            slurm_path=os.path.join(current_path,sub_entry)


    if is_slurm and is_inp:
        global Stru_E_Pair_Dict
        # rename
        global Rename
        global InputDir
        global stru_savepath
        try:
            if Rename == True:
                new_name="_".join(current_path.split("/")[current_path.split("/").index(InputDir.split("/")[-1])+1:])+".xyz"
            else:
                new_name=os.path.basename(inp_path).split(".")[0]+".xyz"

            new_basename=new_name.split(".")[0]
            #xyz
            xyz_str=""
            with open(inp_path,"r") as f:
                inplist=f.readlines()
                f.close()
            start=False;end=True;gather=[];num=-1;electron=0

            for l in inplist:
                xyz_l=l
                if l[0]=="*":
                    if "xyz" in l:
                        start=True
                        electron=int(l.split()[2])
                        xyz_l="{} {} {}\n".format(new_basename,l.split()[2],l.split()[3])
                if start==True and end==True:
                    if len(l)<5:
                        end=False
                        gather.insert(0,f"{num}\n")
                if start and end:
                    num+=1
                    gather.append(xyz_l)
            xyz_str="".join(gather)
            #judge type (nu,ps,ng)
            type_ = "nu"
            if electron==-1:
                type_="ng"
            elif electron==1:
                type_="ps"

            #find energy
            is_energy=False
            with open(slurm_path,"r") as f:
                slulist=f.readlines()
                f.close()
            for li in slulist:
                if "FINAL SINGLE POINT ENERGY" in li:
                    Energy = float(li.split()[-1]) * 27.2113863
                    is_energy=True

            #Update Dict and write xyz file
            if (not new_name in Stru_E_Pair_Dict.keys()) and is_energy:
                Stru_E_Pair_Dict[new_name]=[Energy,type_]
                print(f"New item:{new_basename}-------------{Energy}")
                with open(os.path.join(stru_savepath,type_,new_name),"w") as f:
                    f.write(xyz_str)
                    f.close()
            pass
        except:
            print(f"Error with {current_path}")



parser=argparse.ArgumentParser()
parser.add_argument("-o",default="./stru_energy")
parser.add_argument("-i")
parser.add_argument('-r',default=True)

if __name__=="__main__":
    args=parser.parse_args()

    OutputDir=args.o
    InputDir=args.i.replace("\\","/")
    Rename=args.r

    #


    #
    if not os.path.exists(OutputDir):
        try:
            os.mkdir(OutputDir)
        except:
            raise ValueError(f"Cannot mkdir {OutputDir}")

    stru_savepath = os.path.join(OutputDir, "structures")

    if not os.path.exists(stru_savepath):
        os.mkdir(stru_savepath)

    if not os.path.exists(os.path.join(stru_savepath,"nu")):
        os.mkdir(os.path.join(stru_savepath,"nu"))

    if not os.path.exists(os.path.join(stru_savepath,"ps")):
        os.mkdir(os.path.join(stru_savepath,"ps"))

    if not os.path.exists(os.path.join(stru_savepath,"ng")):
        os.mkdir(os.path.join(stru_savepath,"ng"))


    #
    SEP_Str=""
    if os.path.exists(os.path.join(OutputDir,"Stru_E_Pair.json")):
        with open(os.path.join(OutputDir,"Stru_E_Pair.json"),"r") as f:
            Stru_E_Pair_Dict=json.load(f)

    #Input ****** Process
    travel_(InputDir,judge_and_deal)
    with open(os.path.join(OutputDir, "Stru_E_Pair.json"), "w") as f:
        json.dump(Stru_E_Pair_Dict,f)
        f.close()

    nu_list = [];ng_list = [];ps_list = []
    
    for key in Stru_E_Pair_Dict.keys():
        t = tuple([key, Stru_E_Pair_Dict[key][0]])
        typ=Stru_E_Pair_Dict[key][1]
        if "ps" == typ:
            ps_list.append(t)
        elif "ng" == typ:
            ng_list.append(t)
        else:
            nu_list.append(t)

    with open(os.path.join(OutputDir,"SEP_nu.csv"),"w") as fnu:
        writer_nu=csv.writer(fnu)
        writer_nu.writerows(nu_list)
        fnu.close()

    with open(os.path.join(OutputDir, "SEP_ps.csv"),"w") as fps:
        writer_ps = csv.writer(fps)
        writer_ps.writerows(ps_list)
        fps.close()

    with open(os.path.join(OutputDir, "SEP_ng.csv"),'w') as fng:
        writer_ng = csv.writer(fng)
        writer_ng.writerows(ng_list)
        fng.close()
