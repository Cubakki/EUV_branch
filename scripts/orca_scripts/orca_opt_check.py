import os
import sys
import shutil

Check_dir_path=["./orca_workdir"]
if __name__=="__main__":
    #Load Done
    done_list=[]
    if not os.path.exists("./Done.log"):
        f=open("./Done.log","w",encoding="utf-8")
        f.write("")
        f.close()
    with open("./Done.log","r") as f:
        done_list=f.readlines()
        f.close()

    done_list=[s.strip() for s in done_list]

    #Check Done
    new_done_list=[]
    for root_path in Check_dir_path:
        for stru in os.listdir(root_path):
            if stru in done_list:
                pass
            stru_dir = root_path + f"/{stru}"
            complete_flag = False
            for file in os.listdir(stru_dir):
                if "slurm" in file:
                    with open(stru_dir + f"/{file}", "r") as f:
                        if "****ORCA TERMINATED NORMALLY****" in f.readlines()[-2]:
                            complete_flag = True
    #Cache Done
            if complete_flag==True:
                #os.system(f"echo {complete_flag} | u paste")
                new_done_list.append(stru)
    #Write Done

    with open("./Done.log", "w",encoding="utf-8") as f:
        f.write("\n".join(new_done_list))
        f.close()

    print("已有{}个完成的计算:".format(len(new_done_list)))
    print('\n'.join(new_done_list))