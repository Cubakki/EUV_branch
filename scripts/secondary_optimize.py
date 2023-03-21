import os
from shutil import copy as cp
import random
'''
需要给出运行完成的VASP工作目录，函数将此目录中的CONTCAR和必要文件复制至程序根目录下或{指定文件夹}中并运行pbs脚本进行二次优化
Need to be provided with the VASP workdir which had been finished running,the function will copy CONTACR and necessary
files to the root directory or {specified directory},then apply the pbs
'''




def sec_opt(vasp_workdir,pbs_script_name="intel_vasp6.2_2017.pbs",sec_workdir="./sec_VASP_workdir"):
    '''
    Need to be provided with the VASP workdir which had been finished running,the function will copy CONTACR and necessary
    files to the root directory or {specified directory},then apply the pbs
    :param vasp_workdir:
    :param sec_workdir:
    :return: True
    '''

    '''
    检查vasp工作目录中的主要文件&Check important files in the VASP workdir
    '''
    if os.path.exists(f"{vasp_workdir}/CONTCAR")  \
    and os.path.exists(f"{vasp_workdir}/INCAR") \
    and os.path.exists(f"{vasp_workdir}/KPOINTS") \
    and os.path.exists(f"{vasp_workdir}/{pbs_script_name}"):
        pass
    else:
        raise TypeError("Lacking necessary files in specified VASP workdir")

    '''
    创建新目录并移动文件
    create new directory and move the files
    '''
    if not os.path.exists(sec_workdir):
        os.mkdir(sec_workdir)
    new_wkpath=sec_workdir+"/"+vasp_workdir
    os.mkdir(new_wkpath)
    cp(f"{vasp_workdir}/CONTCAR",f"{new_wkpath}/POTCAR")
    cp(f"{vasp_workdir}/INCAR",f"{new_wkpath}")
    cp(f"{vasp_workdir}/KPOINTS", f"{new_wkpath}")
    cp(f"{vasp_workdir}/{pbs_script_name}", f"{new_wkpath}")

    '''
    创建并运行bash脚本，提交pbs任务
    create and run a bash script to commit the pbs task
    '''

    bash_text = f"echo \" in bash-->target_dir:{new_wkpath}\"\n" \
                f"cd {new_wkpath}\n" \
                f"qsub {pbs_script_name}\n" \
                f"echo \"已执行:qsub {pbs_script_name}\""
    # print(bash_text)
    b_name = f"tem{random.randint(10000000,99999999)}.sh"
    f = open(b_name, 'w')
    f.write(bash_text)
    f.close()
    os.system(f"bash {b_name}")

    print(f"已成功提交{vasp_workdir}的二次优化任务")


if __name__=="__main__":
    for dirs in os.listdir("./VASP_workdir"):
        sec_opt(dirs)