

#本程序用于提取orca计算结果中的FINAL SINGLE POINT ENERGY部分
import os

PATH="./SnCHO_CLP/ACDMSN_SnCHO/1/PES/orca_dir"

if __name__=="__main__":
    lenth_energy_dict={}
    energy_list=[]
    for dir in os.listdir(PATH):
        cal_dir_path=PATH+f"/{dir}"
        lenth=dir.replace("p",".")
        for file in os.listdir(cal_dir_path):
            if not "slurm" in file:
                continue
            f=open(cal_dir_path+f"/{file}")
            lines=f.readlines()
            f.close()
            for li in lines:
                if "FINAL SINGLE POINT ENERGY" in li:
                    Energy=float(li.split()[-1])
                    lenth_energy_dict[lenth]=Energy
                    energy_list.append(Energy)
    print(f"键长-能量:{lenth_energy_dict}")
    print(f"能量列表:{energy_list}")
    with open("Energy_Result.txt","w",encoding="utf-8") as f:
        f.write(" ".join([str(x) for x in energy_list]))