import os
import shutil

work_log_path="./worked.log"
source_path="./orca_sn_dm/SnCHO_flitered"
apart_path="./SnCHO"

if __name__=="__main__":
    if not os.path.exists(apart_path):
        os.mkdir(apart_path)

    with open(work_log_path,"r") as f:
        worked_list=[x.strip() for x in f.readlines()]
        f.close()

    i=0
    for structure in os.listdir(source_path):
        i+=1
        if i>=300:
            break
        stru_path=source_path+f"/{structure}"
        if not structure.split(".")[0] in worked_list:
            worked_list.append(structure.split(".")[0])
            shutil.copy(stru_path,apart_path)

    with open("./worked1.log","w",encoding="utf-8") as f:
        f.write("\n".join(worked_list))
        f.close()