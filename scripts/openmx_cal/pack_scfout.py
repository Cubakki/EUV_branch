import os
import shutil


WORK_ROOT = "./openmx_workdir"
PACK_ROOT = "./openmx_Si_pack"

if __name__ == "__main__":
    i = 0
    error = []
    for chdir in os.listdir(WORK_ROOT):
        chd_scf_path = WORK_ROOT + "/" + chdir + "/" + "openmx.scfout"
        if os.path.exists(chd_scf_path):
            with open(chd_scf_path, "r",encoding = "latin1") as f:
                try:
                    keyline = f.readlines()[-1]
                    print(keyline)
                    if "Others" in keyline:
                        print(f"{chdir} normally end.")
                        transfer_path = PACK_ROOT + "/" + chdir + "/"
                        if not os.path.exists(transfer_path):
                            os.makedirs(transfer_path)
                        shutil.copy(chd_scf_path, transfer_path)
                        i+=1
                except:
                    print(f"Some error occurs when dealing with {chd_scf_path}")
                    error.append(chdir)

    print(f"{i} pack scfouts end.Move them in {PACK_ROOT}")
    print("Errors : {}".format(" ".join(error)))