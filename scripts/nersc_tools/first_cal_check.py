#检查first_calculation中orca_workdir内的计算结果是否成功，删去不成功的计算目录并同步worked

import os
import shutil

Workdir="./orca_workdir"
if __name__=="__main__":
    Error_list = []
    Done_list = []

    if os.path.exists("./done.log"):
        with open ("./done.log","r") as f:
            Done_list = [x.strip() for x in f.readlines()]
            f.close()

    for stru in os.listdir(Workdir):
        if stru in Done_list:
            continue
        stru_dir=Workdir+f"/{stru}"
        try:
            if os.path.exists(stru_dir + "/output.log"):
                with open(stru_dir + "/output.log", "r") as f:
                    if "****ORCA TERMINATED NORMALLY****" in f.readlines()[-2]:
                        Done_list.append(stru)
                    else:
                        print(f"{stru} was not correctly finished")
                        Error_list.append(stru)
            else:
                print(f"{stru} was not correctly finished")
                Error_list.append(stru)
        except:
            print(f"{stru} occurs an unkown error")
            Error_list.append(stru)
            #input()

    print("Check end, {} worked, {} done, {} error.".format(len(os.listdir(Workdir)),len(Done_list),len(Error_list)))
    with open("./Error_Terminated.err", "w", encoding="utf-8") as m:
        m.write("\n".join(Error_list))
        m.close()

    with open("./done.log",'w',encoding="utf-8") as f:
        f.write("\n".join(Done_list))
        f.close()


    delete = input(
        "If you want to delete the uncompleted calculation directories and rewrite worked.log , please type \'yes\'")
    if delete == "yes":
        for err in Error_list:
            del_path = Workdir+f"/{err}"
            shutil.rmtree(del_path)
            print(Workdir+f"/{err} was not correctly finished, delete.")
        with open("./worked.log","w",encoding="utf-8") as f:
            f.write("\n".join(Done_list))
            f.close()