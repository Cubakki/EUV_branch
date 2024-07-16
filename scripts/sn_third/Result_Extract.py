#提取结果
import copy

import xlrd,xlwt
#本程序用于提取orca计算结果中的FINAL SINGLE POINT ENERGY部分
import os
import json
#find dissociation energy<0 added

PATH= "./workdir"
OUTPUT_PATH="./excel_data"

def formula(ele):
    'from atom ele generate formula'
    fd={'Sn':0,"C":0,"H":0,"O":0}
    for x in ele:
        if not x in fd.keys():
            fd[x]=0
        fd[x]+=1
    formula_="Sn{}C{}H{}O{}".format(fd['Sn'],fd['C'],fd['H'],fd['O'])
    return formula_

if __name__=="__main__":
    whole_dict={}
    Less_than_zero={}
    for stru in os.listdir(PATH):
        try:
            stru_path=PATH+f"/{stru}"
            r_dict={}
            #read scope
            nu_file=open(stru_path+"/nu.xyz","r")
            fc=nu_file.readlines()
            atom_num=int(fc[0].strip())
            atom_ele=[x.strip().split(" ")[0].strip() for x in fc[2:]]
            r_dict["atom_num"]=atom_num
            r_dict["atom_ele"]=atom_ele
            r_dict["formula"] = formula(atom_ele)
            r_dict["splits"] = []
            #initial structure
            ini_path=stru_path+"/initial"
            for state in ["nu", "ng", "ps"]:
                inist_path=ini_path+f"/{state}"
                for file in os.listdir(inist_path):
                    if not "slurm" in file:
                        continue
                    f = open(inist_path + f"/{file}","r",encoding="utf-8")
                    lines = f.readlines()
                    f.close()
                    for li in lines:
                        if "FINAL SINGLE POINT ENERGY" in li:
                            Energy = float(li.split()[-1])*27.2113863
                            r_dict[f"initial_{state}_energy"]=Energy
            #Ionization and Electron Attachment
            Ionization_Energy=r_dict["initial_ps_energy"]-r_dict["initial_nu_energy"]
            Electron_Attachment_Energy=r_dict["initial_ng_energy"]-r_dict["initial_nu_energy"]
            r_dict["Ionization_Energy"]=Ionization_Energy
            r_dict["Electron_Attachment_Energy"]=Electron_Attachment_Energy

            #seperated structure
            for state in ["nu","ng","ps"]:
                state_path=stru_path+f"/{state}"
                for pattern in os.listdir(state_path):
                    pattern_path=state_path+f"/{pattern}"
                    for sit in os.listdir(pattern_path):
                        Energy_cl=[]
                        if not "." in sit:  #find directroies
                            cl_path=pattern_path+f"/{sit}"
                            c_path,l_path=cl_path+"/core_cal",cl_path+"/ligand_cal"
                            for cal_dir_path in [c_path,l_path]:
                                for file in os.listdir(cal_dir_path):
                                    if not "slurm" in file:
                                        continue
                                    f=open(cal_dir_path+f"/{file}","r",encoding="utf-8")
                                    lines=f.readlines()
                                    f.close()
                                    for li in lines:
                                        if "FINAL SINGLE POINT ENERGY" in li:
                                            Energy_cl.append((float(li.split()[-1])*27.2113863))
                            single_split_dict = {}
                            single_split_dict[f"{state}_{pattern}_{sit}_energy"] = sum(Energy_cl)
                            single_split_dict[f"{state}_{pattern}_{sit}_split"] = r_dict[f"{state}_{pattern}_{sit}_energy"]-r_dict[f"initial_{state}_energy"]
                            r_dict["splits"].append(copy.deepcopy(single_split_dict))
                            if single_split_dict[f"{state}_{pattern}_{sit}_split"]<0:
                                print(f"Find dissociation energy < 0:{stru}_{state}_{pattern}_{sit}_split"+"="+str(r_dict[f"{state}_{pattern}_{sit}_split"]))
                                Less_than_zero[f"{stru}_{state}_{pattern}_{sit}_split"]=copy.deepcopy(single_split_dict[f"{state}_{pattern}_{sit}_split"])
                with open("../Energy_Result.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join([str(x+" "+str(y))for x,y in r_dict.items()]))
            ##############excel operation
            excel_name=f"{stru}.xls"
            wb=xlwt.Workbook(encoding="ascii")
            wsheet=wb.add_sheet("Sheet1")
            i=0
            for key,value in r_dict.items():
                wsheet.write(0,i,key)
                wsheet.write(1,i,value)
                i+=1
            if not os.path.exists(OUTPUT_PATH):
                os.mkdir(OUTPUT_PATH)
            wb.save(f"{OUTPUT_PATH}/{excel_name}")
            whole_dict[stru]=copy.deepcopy(r_dict)
        except:
            print(f"{stru} process error")

    #Save less than zero
    excel_name = f"Less_than_zero.xls"
    wb = xlwt.Workbook(encoding="ascii")
    wsheet = wb.add_sheet("Sheet1")
    i = 0
    for key, value in Less_than_zero.items():
        wsheet.write(0, i, key)
        wsheet.write(1, i, value)
        i += 1
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    wb.save(f"{OUTPUT_PATH}/{excel_name}")
    #Save json
    data_file=open("./data.json","w",encoding="utf-8")
    json.dump(whole_dict,data_file)
    print("json data saved.")