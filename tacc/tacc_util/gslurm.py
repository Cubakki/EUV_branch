#slurm_generator


class Slurm_generator:
    def __init__(self,block=""):
        self.n=0
        self.head="#!/bin/bash\n"\
                "#SBATCH --nodes=2\n"\
                "#SBATCH -t 24:00:0\n"\
                f"##SBATCH -n {self.n}\n"\
                "##SBATCH --cpus-per-task=1\n"\
                "#SBATCH --ntasks-per-node=48\n"\
                "#SBATCH --partition=normal\n"\
                "##SBATCH --oversubscribe\n"\
                +block\
                +"\n"
        self.middle="module purge\n"\
                    "# openmpi 4.1.1\n"\
                    "module load intel/19.1.1\n"\
                    "export PATH=/home1/04542/tg838412/work2/src/openmpi-4.1.1/install/bin:/home1/04542/tg838412/work2/src/orca_5_0_4_linux_x86-64_shared_openmpi411:$PATH\n"\
                    "export LD_LIBRARY_PATH=/home1/04542/tg838412/work2/src/openmpi-4.1.1/install/lib:$LD_LIBRARY_PATH:/home1/04542/tg838412/work2/src/orca_5_0_4_linux_x86-64_shared_openmpi411\n"\
                    "\n"\
                    "pwd=`pwd`\n"\
                    "\n"

        self.body=""
        self.tail="\n"\
            "wait\n"

    def __add_n__(self,n=1):
        self.n+=n
        self.head="#!/bin/bash\n"\
                f"#SBATCH --nodes={self.n}\n"\
                "#SBATCH -t 24:00:0\n"\
                f"##SBATCH -n {self.n}\n"\
                "##SBATCH --cpus-per-task=1\n"\
                "#SBATCH --ntasks-per-node=48\n"\
                "#SBATCH --partition=normal\n"\
                "##SBATCH --oversubscribe\n"

    def add_subtask(self,lines):
        self.body+=lines
        self.__add_n__()

    def generate(self,path):
        '''

        :param path: include file name
        :return:
        '''
        self.output=self.head+self.middle+self.body+self.tail
        with open(path,"w",encoding="utf-8") as c:
            c.write(self.output)
        return self.output


if __name__=="__main__":
    s=Slurm_generator()