import argparse
import os
import shutil
from orca_utils.orca_writer import ORCA_INPUT
from orca_utils.bash_generator import bash_g
from orca_utils.utils import calculate_electron_num

'''
用于(ORCA)对一系列xyz文件进行结构优化
'''

File_path = ""
Work_path = "./orca_workdir"

################################  Parser
import sys

parser = argparse.ArgumentParser()

parser.add_argument("-f", default="./resources/SnCHO_flitered")
parser.add_argument("-p", default="PBS")
parser.add_argument("-n", default=20)

args = parser.parse_args()
################################

################################ load worked structure
with open("../worked.log", "r", encoding="utf-8") as fr:
    worked = fr.readlines()
    fr.close()
    worked = [x.strip() for x in worked]
################################


if __name__ == "__main__":
    File_path = args.f
    Submit_num = int(args.n)
    Platform = args.p

    if args.p == "PBS":
        submit_script_name = "orca.pbs"
    elif args.p == "Slurm":
        submit_script_name = "orca.slm"
    else:
        print("-p platform needed to be \"PBS\" or \"Slurm\"")
        sys.exit()

    if not os.path.exists(Work_path):
        os.mkdir(Work_path)
    submited = 0
    for stru_f in os.listdir(File_path):
        added = 0
        try:
            if not submited < Submit_num:
                break
            wd_name = stru_f.split(".")[0]
            if wd_name in worked:
                continue
            else:
                worked.append(wd_name)
                submited += 1
                added = 1
            wd_path = Work_path + f"/{wd_name}"
            stru_path = wd_path + f"/{stru_f}"
            if not os.path.exists(wd_path):
                os.mkdir(wd_path)
            # 拷贝结构文件至其工作目录
            shutil.copy(File_path + f"/{stru_f}", wd_path)
            ele_num = calculate_electron_num(stru_path)
            # 生成inp文件
            if Platform == "Slurm":
                input_generator = ORCA_INPUT("!TPSS DEF2-SVP D3BJ OPT", stru_path, ele_num, 0,
                                             ["% PAL NPROCS 16 END\n"])
            else:
                input_generator = ORCA_INPUT("!TPSS DEF2-SVP D3BJ OPT", stru_path, ele_num, 0, ["% PAL NPROCS 16 END\n"])
            input_generator.write(wd_path + "/input.inp")
            # 拷贝脚本文件
            shutil.copy(f"./orca_utils/{submit_script_name}", wd_path)
            # 生成bash
            bash_path = bash_g(wd_path, Platform, submit_script_name)
            os.system(f"bash {bash_path}")
            os.remove(bash_path)
            print("已提交优化{}".format(wd_name))
        except:
            if added == 1:
                worked.pop()
                submited -= 1
            print("Error with submitting {}".format(stru_f))
    with open("../worked.log", "w", encoding="utf-8") as fw:
        fw.write("\n".join(worked))
        fw.close()
    print("Program Exit.")
