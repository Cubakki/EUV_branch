import os
import shutil
import argparse
import sys

from orca_utils.orca_writer import ORCA_INPUT
from orca_utils.bash_generator import bash_g
from orca_utils.utils import calculate_electron_num

# parse
parser = argparse.ArgumentParser()

parser.add_argument("-f", default="./structures")
parser.add_argument("-p", default="PBS")
parser.add_argument("-n", default=20)

args = parser.parse_args()

# default args
structure_path = "./structures"
work_path = "./orca_workdir"

if __name__ == "__main__":
    # args
    n = int(args.n)
    platform = args.p
    if not platform in ["PBS", "Slurm"]:
        print("-p need to be PBS or Slurm")
        sys.exit()
    platform_sdict = {"PBS": "./orca_utils/orca.pbs", "Slurm": "./orca_utils/orca.slm"}
    script_name=platform_sdict[platform].split("/")[-1]
    # path check
    if not os.path.exists(work_path):
        os.mkdir(work_path)
    # Load worked
    if not os.path.exists("worked.log"):
        with open("./worked.log", "w", encoding="utf-8") as f:
            f.write("")
            f.close()
    with open("./worked.log", "r") as f:
        worked_list = f.readlines()
        f.close()

    i=0
    # Load structures
    for stru in os.listdir(structure_path):
        if i>=n:
            break
        stru_path = structure_path + f"/{stru}" + f"/{stru}.xyz"
        # Check if worked
        if not stru in worked_list:
            # Create workdir

            st_work_path = work_path + f"/{stru}"
            if not os.path.exists(st_work_path):
                os.mkdir(st_work_path)
            shutil.copy(stru_path, st_work_path + f"/nu.xyz")
            nu_path = st_work_path + f"/nu.xyz"
            ng_dir = st_work_path + f"/ng"
            ps_dir = st_work_path + f"/ps"
            # check
            if not os.path.exists(ng_dir):
                os.mkdir(ng_dir)
            if not os.path.exists(ps_dir):
                os.mkdir(ps_dir)
            # copy neutral file into ng&ps dir
            shutil.copy(nu_path, ng_dir + "/")
            shutil.copy(nu_path, ps_dir + "/")
            # copy slm&pbs script
            shutil.copy(platform_sdict[platform], ng_dir + "/")
            shutil.copy(platform_sdict[platform], ps_dir + "/")
            # input generate
            ng_gen = ORCA_INPUT("!TPSS DEF2-SVP D3BJ OPT", ng_dir + "/nu.xyz",
                                calculate_electron_num(ng_dir + "/nu.xyz"),
                                -1, ["% PAL NPROCS 16 END\n"])
            ng_gen.write(ng_dir + "/input.inp")
            ps_gen = ORCA_INPUT("!TPSS DEF2-SVP D3BJ OPT", ps_dir + "/nu.xyz",
                                calculate_electron_num(ps_dir + "/nu.xyz"),
                                1, ["% PAL NPROCS 16 END\n"])
            ps_gen.write(ps_dir + "/input.inp")
            #generate bash
            ng_bp=bash_g(ng_dir,platform,script_name)
            ps_bp=bash_g(ps_dir,platform,script_name)
            #run bash
            os.system(f"bash {ng_bp}")
            os.system(f"bash {ps_bp}")
            #hint
            print("Succeed submit {}'s ng/ps opt".format(stru))
            #add worked
            worked_list.append(stru)
            i+=1

    print("Succeeded to submit {} couple of tasks.".format(i))
    with open("./worked.log","w",encoding="utf-8")as f:
        f.write("\n".join(worked_list))
        f.close()
    print("worked.log saved.Program Exit.")