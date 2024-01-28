import os
import sys
import shutil

Check_dir_path=["../orca_sn_sec/orca_workdir"]
if __name__=="__main__":
    # Check Done
    path_dict={}
    wrong_list = []
    i=0
    for root_path in Check_dir_path:
        for stru in os.listdir(root_path):
            stru_dir = root_path + f"/{stru}"
            ng_complete_flag = False
            ps_complete_falg = False
            ng_dir, ps_dir = stru_dir + f"/ng", stru_dir + f"/ps"
            for file in os.listdir(ng_dir):
                if "slurm" in file:
                    with open(ng_dir + f"/{file}", "r") as f:
                        if "****ORCA TERMINATED NORMALLY****" in f.readlines()[-2]:
                            ng_complete_flag = True
            for file in os.listdir(ps_dir):
                if "slurm" in file:
                    with open(ps_dir + f"/{file}", "r") as f:
                        if "****ORCA TERMINATED NORMALLY****" in f.readlines()[-2]:
                            ps_complete_flag = True

            complete_flag = ps_complete_flag and ng_complete_flag
            # Cache Done
            if not complete_flag == True:
                # os.system(f"echo {complete_flag} | u paste")
                wrong_list.append(stru)
                path_dict[stru] = stru_dir
                print(f"{stru} calculation wrong")
                i+=1

    #Check End
    print("Check Done.There are {} wrong calculations:{}\n Do you want to modify worked.log and delect the work diretory?\nprint Yes or No".format(i,wrong_list))
    exe=input()
    if exe=="Yes":
        print("Executing modify...")
        with open("./worked.log", "r") as f:
            worked_list = f.readlines()
            f.close()
        new_wlist=[]
        worked_list=[x.strip() for x in worked_list]
        for it in worked_list:
            if not it in wrong_list:
                new_wlist.append(it)
            else:
                print("Worked remove {}".format(it))
                shutil.rmtree(path_dict[it])
        with open("./worked.log", "w") as f:
            f.write("\n".join(new_wlist))
            f.close()
        print("Modify End.")
    else:
        print("Giving up modify.")
