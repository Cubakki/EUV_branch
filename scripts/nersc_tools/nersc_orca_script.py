import argparse
import os
import shutil
from orca_utils.orca_writer import ORCA_INPUT
from orca_utils.bash_generator import bash_g
from orca_utils.utils import calculate_electron_num
from orca_utils.sbatch_generator import Sbatch_Generator

'''
用于(ORCA)对一系列xyz文件进行结构优化
'''

#Just show, nothing will happen if you change the values below, for they will reinit after argument parse.
File_path = "./structure"
Work_path = "./orca_workdir"
Nodes = 32
Core_per_node = 128
Core_per_task = 8
Tasks_per_node = int(Core_per_node / Core_per_task)
Tasks_in_all = int(Nodes * Tasks_per_node)


################################  Parser
import sys

parser = argparse.ArgumentParser()

parser.add_argument("-f", default="./structures")
parser.add_argument("-w", default="./orca_workdir")
parser.add_argument("-p", default="Slurm")
parser.add_argument("-N", default=32)
parser.add_argument("-cpn", default=128)
parser.add_argument("-cpt", default=8)
parser.add_argument("-n", default=20)

args = parser.parse_args()
################################


################################ check if there is a work log
if not os.path.exists("./worked.log"):
    with open("./worked.log", 'w') as f:
        f.close()
################################ load worked structure
with open("./worked.log", "r", encoding="utf-8") as fr:
    worked = fr.readlines()
    fr.close()
    worked = [x.strip() for x in worked]
################################

def declare_settings():
    print("Below is the settings:" + "\n"
                                     "Using_Nodes: " + str(Nodes) + "\n"
                                                                    "Core_per_node: " + str(Core_per_node) + "\n"
                                                                                                             "Core_per_task: " + str(
        Core_per_task) + "\n"
                         "Tasks_per_node: " + str(Tasks_per_node) + "\n"
                                                                    "Tasks_in_all: " + str(Tasks_in_all) + "\n"
                                                                                                           "Work_path: " + str(
        Work_path) + "\n"
                     "File_path: " + str(File_path) + "\n")


def set_platform():
    if Platform == "PBS":
        submit_script_name = "orca.pbs"
    elif Platform == "Slurm":
        submit_script_name = "orca.slm"
    else:
        print("-p platform needed to be \"PBS\" or \"Slurm\"")
        sys.exit()


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)


def setup_one_job(input_structure_path: str):
    """
    orgnize all files and directory for one job, and return its slurm job block
    :return:
    """
    with open(input_structure_path, "r", encoding="utf-8") as fr:
        lines = fr.readlines()
        fr.close()
    structure_name = input_structure_path.split("/")[-1].split(".")[0]
    workdir_path = Work_path + "/" + structure_name
    structure_file_path = workdir_path + "/" + input_structure_path.split("/")[-1]
    check_path(workdir_path)
    # 拷贝结构文件至其工作目录
    shutil.copy(input_structure_path, workdir_path)
    electron_num = calculate_electron_num(structure_file_path)
    # 生成inp文件
    input_generator = ORCA_INPUT("!TPSS DEF2-SVP D3BJ OPT", structure_file_path, electron_num, 0,
                                     ["% PAL NPROCS {} END\n".format(Core_per_task)])
    input_generator.write(workdir_path + "/input.inp")
    #生成job block
    job_block=("podman-hpc run \\\n"
               "--rm \\\n")
    job_block += "--volume=/pscratch/sd/w/wangh/orca:/orca \\\n"
    job_block += "--volume={}:/orca_workdir \\\n".format(workdir_path)
    job_block += "--workdir=/orca \\\n"
    job_block += "--cpus={} \\\n".format(Core_per_task)
    job_block += "--shm-size=10240M \\\n"
    job_block += "--env OMPI_ALLOW_RUN_AS_ROOT=1 \\\n"
    job_block += "--env OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1 \\\n"
    job_block += "docker.io/stephey/orca:3.0 ./orca /orca_workdir/input.inp > {}/output.log 2>&1 &\n\n".format(workdir_path)

    return job_block

if __name__ == "__main__":
    File_path = args.f
    Work_path = args.w
    Platform = args.p
    Nodes = int(args.N)
    Core_per_node = int(args.cpn)
    Core_per_task = int(args.cpt)

    #Submit_num = int(args.n)
    Tasks_per_node = int(Core_per_node / Core_per_task)
    Tasks_in_all = int(Nodes * Tasks_per_node)

    declare_settings()
    set_platform()

    #Workdir Check
    check_path(Work_path)

    #Sbatch init
    sbatch_generator = Sbatch_Generator()
    settings=["-A m3551","-C cpu","-q regular","-t 24:00:00","-N {}".format(Nodes)]
    sbatch_generator.add_settings(settings)
    sbatch_generator.add_job("\nulimit -s 100000\n")

    #Generate candidates
    structure_name_list = []
    tail_corresponding = {}
    for file_name in os.listdir(File_path):
        structure_name_list.append(file_name.split(".")[0])
        tail_corresponding[file_name.split(".")[0]] = file_name.split(".")[1:]
    candidates = list(set(structure_name_list) - set(worked))
    if len(candidates)==0:
        print("No candidates found,exit.")
        sys.exit()

    submit_in_all=0
    submit_stru_this_trun=[]
    candidate_end = False
    while submit_in_all < Tasks_in_all:
        submit_in_node=0
        node_block = "srun -N 1 bash -c \""
        while submit_in_node < Tasks_per_node:
            current_block = ""
            for candidate in candidates:
                if candidate == candidates[-1]:
                    candidate_end = True
                print("currnet_candidate : {}".format(candidate))
                candidate_file_path = File_path+"/"+candidate+"."+".".join(tail_corresponding[candidate])
                try:
                    current_block=setup_one_job(candidate_file_path)
                    print("{} set up successfully".format(candidate))
                    submit_in_node += 1
                    submit_in_all += 1
                    candidates.remove(candidate)
                    worked.append(candidate)
                    submit_stru_this_trun.append(candidate)
                    break
                except:
                    current_block = ""
                    continue
            node_block += current_block
            if candidate_end == True:
                break
        node_block += "wait\" &\n"
        sbatch_generator.add_job(node_block)
        if candidate_end == True:
            break
    sbatch_generator.add_job("wait\n")

    sbatch_generator.export(os.path.join(Work_path,"tem.slm"))
    os.system("sbatch {}".format(os.path.join(Work_path,"tem.slm")))
    os.remove(os.path.join(Work_path,"tem.slm"))
    print("All jobs done!Submit {} child jobs in all, structure names are:\n{}".format(len(submit_stru_this_trun),",".join(submit_stru_this_trun)))

    #write worked log
    with open("./worked.log", "w", encoding="utf-8") as fw:
        fw.write("\n".join(worked))
        fw.close()

    print("Program Exit.")