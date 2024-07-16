import os
#Check if the output files are correct(ORCA terminated normally)
Workdir="./orca_workdir"
if __name__=="__main__":
    Error_list = []
    checked_list = []
    for stru in os.listdir(Workdir):
        stru_dir=Workdir+f"/{stru}"
        complete_flag=False
        for file in os.listdir(stru_dir):
            if "slurm" in file:
                with open(stru_dir + f"/{file}", "r") as f:
                    if "****ORCA TERMINATED NORMALLY****" in f.readlines()[-2]:
                        complete_flag = True
                    # else:
                    #     os.remove(f"{stru_dir}/{file}")
        if complete_flag == False:
            print(f"{stru} was not correctly finished")
            Error_list.append(stru)
    with open("./Error_Terminated.err", "w", encoding="utf-8") as m:
        m.write("\n".join(Error_list))
        m.close()

