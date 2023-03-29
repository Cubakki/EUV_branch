import argparse
import os
import shutil
from orca_utils.orca_writer import ORCA_INPUT
from orca_utils.bash_generator import bash_g

'''
用于(ORCA)对一系列xyz文件进行结构优化
'''

File_path=""
Work_path="./orca_workdir"

################################  Parser
import sys

parser=argparse.ArgumentParser()

parser.add_argument("-f",default="./resources/SnCHO_flitered")

args=parser.parse_args()
################################

if __name__=="__main__":
    File_path=args.f
    if not os.path.exists(Work_path):
        os.mkdir(Work_path)
    for stru_f in os.listdir(File_path):
        wd_name=stru_f.split(".")[0]
        wd_path=Work_path+f"/{wd_name}"
        if not os.path.exists(wd_path):
            os.mkdir(wd_path)
        #拷贝结构文件至其工作目录
        shutil.copy(File_path+f"/{stru_f}",wd_path)
        #生成inp文件
        input_generator=ORCA_INPUT("!TPSS DEF2-SVP D3BJ OPT",wd_path+f"/{stru_f}",0,["% PAL NPROCS 4 END\n"])
        input_generator.write(wd_path+"/input.inp")
        #拷贝pbs脚本文件
        shutil.copy("./orca_utils/orca.pbs",wd_path)
        #生成bash
        bash_path=bash_g(wd_path,"PBS","orca.pbs")
        os.system(f"bash {bash_path}")
        os.remove(bash_path)
        print("已提交优化{}".format(wd_name))
