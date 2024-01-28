import os
import sys
import shutil

Check_dir_path=["../orca_sn_sec/orca_workdir"]
Transfer_path="./optimized_structures"
if __name__=="__main__":
    #work_path_validation
    if not os.path.exists(Transfer_path):
        os.mkdir(Transfer_path)
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
    path_dict={}
    new_done_list=[]
    for root_path in Check_dir_path:
        for stru in os.listdir(root_path):
            if stru in done_list:
                pass
            stru_dir = root_path + f"/{stru}"
            ng_complete_flag = False;ps_complete_flag=False
            ng_dir,ps_dir=stru_dir+f"/ng",stru_dir+f"/ps"
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

            complete_flag=ps_complete_flag and ng_complete_flag
    #Cache Done
            if complete_flag==True:
                #os.system(f"echo {complete_flag} | u paste")
                new_done_list.append(stru)
                path_dict[stru]=stru_dir
    #Write Done

    with open("./Done.log", "w",encoding="utf-8") as f:
        f.write("\n".join(new_done_list))
        f.close()

    #Load transfered
    transfered_list=[]
    if not os.path.exists("./transfered.log"):
        f=open("./transfered.log","w",encoding="utf-8")
        f.write("")
        f.close()
    with open("./transfered.log","r") as f:
        transfered_list=[x.strip() for x in f.readlines()]
        f.close()
    #Validation
    for strus in os.listdir(Transfer_path):
        if not strus in transfered_list:
            print(f"Warning:Transfered List is not matched real files in structure path:{Transfer_path}")
            sys.exit()
        continue
    print("Transfered list validation succeed.")
    #Calculate structures(done) needed to be transfered
    Need_trans=list(set(new_done_list)-set(transfered_list))
    #Apply transfer
    for stru in Need_trans:
        stru_path=path_dict[stru]
        s_trans_path=Transfer_path+f"/{stru}"
        if not os.path.exists(s_trans_path):
            os.mkdir(s_trans_path)
        shutil.copy(stru_path+f"/nu.xyz",s_trans_path+"/nu.xyz")
        shutil.copy(stru_path + "/ng/input.xyz", s_trans_path + "/ng.xyz")
        shutil.copy(stru_path + "/ps/input.xyz", s_trans_path + "/ps.xyz")
        transfered_list.append(stru)
        print(f"Succeed to apply transfer in {stru}")
    #Write_transfered
    with open("./transfered.log", "w",encoding="utf-8") as f:
        f.write("\n".join(transfered_list))
        f.close()
    print("Transfer and Pre_Donecheck complete.")