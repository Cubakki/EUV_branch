import os
import shutil
import time


class control():
    input_file_dir : str
    work_dir = "./VASP_workdir"
    potcar_path : str = "../resources/VASP_Utils/POTCAR"
    incar_path : str  = "../resources/VASP_Utils/INCAR"
    kpoint_path : str = "../resources/VASP_Utils/KPOINTS"
    pbs_path : str    = "../resources/VASP_Utils/intel_vasp6.2_2017.pbs"
    pbs_name : str    = "intel_vasp6.2_2017.pbs"
    name : str


    def __init__(self):
        self.advice = "enjoy the script~"
        self.count  = 0
        pass

    def file_check(self):
        #
        text = ""
        for file in self.file_list:
            text += file + "; "
        print("Existing input files to be dealed with:{}".format(text))
        #

    @property
    def file_list(self):
        return os.listdir(self.input_file_dir)

    def run(self,input_dir=""):
        if not input_dir=="":
            self.input_file_dir=input_dir
        self.file_check()
        if not os.path.exists(self.work_dir):
            os.mkdir(self.work_dir)
        for file in self.file_list:
            file_="".join(file.split(".")[:-1])
            if file_=="":
                file_=file
            file_path=self.input_file_dir+"/"+file_
            self.name=file_
            self.in_loop(file_path)

    def in_loop(self,input_file):
        instance_path=self.work_dir+"/"+self.name
        if not os.path.exists(instance_path):
            os.mkdir(instance_path)
        shutil.copy(input_file,instance_path)
        os.rename(instance_path+"/"+input_file.split("/")[-1],instance_path+"/"+"POSCAR")
        shutil.copy(self.potcar_path,instance_path)
        shutil.copy(self.kpoint_path,instance_path)
        shutil.copy(self.incar_path,instance_path)
        shutil.copy(self.pbs_path,instance_path)
        #由于pbs文件必须在指定目录执行，这里使用bash进入目录进行qsub操作
        bash_name=self.bash_generator(instance_path)
        os.system(f"bash {bash_name}")
        print("成功生成工作目录{}并执行vasp优化任务提交".format(instance_path))
        os.remove(bash_name)
        time.sleep(0.2)
        #.......

    def bash_generator(self,target_dir):
        bash_text=f"echo \" in bash-->target_dir:{target_dir}\"\n" \
                  f"cd {target_dir}\n" \
                  f"qsub {self.pbs_name}\n" \
                  f"echo \"已执行:qsub {self.pbs_name}\""
        #print(bash_text)
        b_name=f"tem{self.count}.sh"
        f=open(b_name,'w')
        f.write(bash_text)
        f.close()
        self.count+=1
        return b_name

if __name__=="__main__":
    controller=control()
    controller.run("./resources/POSCAR_SnCHO_First")