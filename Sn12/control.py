import os
import shutil
import argparse
import sys


################################  Parser

parser=argparse.ArgumentParser()

parser.add_argument("--step",default=0)
parser.add_argument("--p",default="PBS")

args=parser.parse_args()
################################

def bash_g(path,platform,script_name):
    if platform=="PBS":
        order="qsub"
    else:
        order="sbatch"
    bash_text=  f"cd {path}\n" \
                f"{order} {script_name}\n"
    with open(path+"/natzme.sh","w") as f:
        f.write(bash_text)
        f.close()
    return path+"/natzme.sh"


if __name__=="__main__":
    args.step=int(args.step)
    if args.step==0:
        print("No step accquired.Exit.")
        sys.exit()

    if args.p=="PBS":
        submit_script_name="orca.pbs"
    elif args.p=="Slurm":
        submit_script_name="orca.slm"
    else:
        print("-p platform needed to be \"PBS\" or \"Slurm\"")
        sys.exit()

    if args.step==1:
        focused_dirs=["./neg_whole","./neural_whole","./pos_whole"]
        for dir in focused_dirs:
            bash_path=bash_g(dir,args.p,submit_script_name)
            os.system(f"bash {bash_path}")
            os.remove(bash_path)
            print("{} has been submitted".format(dir.split("/")[-1]))

    if args.step==2:
        focused_dirs=["./neg_whole","./neural_whole","./pos_whole"]
        for dir in focused_dirs:
            opt_path = dir + "/RevPBE0_opt"
            os.mkdir(opt_path)
            shutil.copy(dir+"/input.xyz",opt_path+"/Sn12.xyz")
            shutil.copy(dir+"/input.inp",opt_path)
            shutil.copy(dir+"/"+submit_script_name,opt_path)
            with open(opt_path+"/input.inp","r") as f:
                fl=f.readlines()
                f.close()
            fl[0]="!REVPBE0 DE2-SVP D3BJ OPT\n"
            with open(opt_path+"input.inp","w") as f:
                f.write("".join(fl))
            bash_path=bash_g(opt_path,args.p,submit_script_name)
            os.system(f"bash {bash_path}")
            os.remove(bash_path)
            print("{} has been submitted".format("/".join(dir.split("/")[:-2])))

    if args.step==3:
        #
        pass