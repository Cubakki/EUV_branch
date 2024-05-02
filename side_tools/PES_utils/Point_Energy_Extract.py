import xlrd,xlwt
#本程序用于提取orca的PES计算结果中的FINAL SINGLE POINT ENERGY部分
import os

PATH= "./PAG"

if __name__=="__main__":
    for stru in os.listdir(PATH):
        stru_path=PATH+f"/{stru}"
        for pattern in os.listdir(stru_path):
            pattern_path=stru_path+f"/{pattern}"+"/PES/orca_dir"
            lenth_energy_dict={}
            energy_list=[]
            for dir in os.listdir(pattern_path):
                cal_dir_path=pattern_path+f"/{dir}"
                lenth=dir.replace("p",".")
                for file in os.listdir(cal_dir_path):
                    if not "slurm" in file:
                        continue
                    f=open(cal_dir_path+f"/{file}","r")
                    lines=f.readlines()
                    f.close()
                    for li in lines:
                        if "FINAL SINGLE POINT ENERGY" in li:
                            Energy=float(li.split()[-1])
                            lenth_energy_dict[lenth]=Energy
                            energy_list.append(Energy)
            print(f"键长-能量:{lenth_energy_dict}")
            print(f"能量列表:{energy_list}")
            with open("../Energy_Result.txt", "w", encoding="utf-8") as f:
                f.write(" ".join([str(x) for x in energy_list]))
        ##############excel operation
            excel_name=f"{stru}_{pattern}.xls"
            wb=xlwt.Workbook(encoding="ascii")
            wsheet=wb.add_sheet("Sheet1")
            wsheet.write(0,0,"bond_lenth")
            wsheet.write(1,0,"energy")
            i=1
            for key,value in lenth_energy_dict.items():
                wsheet.write(0,i,key)
                wsheet.write(1,i,value)
                i+=1
            wb.save(f"{PATH}/{excel_name}")