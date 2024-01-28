#提取结果
import copy

import xlrd,xlwt
#本程序用于提取orca计算结果中的FINAL SINGLE POINT ENERGY部分
import os
import json
#仅计算电离能和亲合能

FIR_PATH="/dm_data/wh/jingbin/SnHO/first_cal/orca_workdir" #第一步计算内工作目录地址
SEC_PATH= "./orca_workdir" #第二步计算内工作目录地址
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
    for stru in os.listdir(SEC_PATH):
        try:
            stru_path=SEC_PATH+f"/{stru}"
            r_dict={}
            #read scope
            nu_file=open(stru_path+"/nu.xyz","r")
            fc=nu_file.readlines()
            atom_num=int(fc[0].strip())
            atom_ele=[x.strip().split(" ")[0].strip() for x in fc[2:]]
            r_dict["atom_num"]=atom_num
            r_dict["atom_ele"]=atom_ele
            r_dict["formula"]=formula(atom_ele)
            #initial structure
            three_path_dict={}
            #ng&ps path
            three_path_dict["ng"] = stru_path + "/ng"
            three_path_dict["ps"] = stru_path + "/ps"
            three_path_dict["nu"] = FIR_PATH  + f"/{stru}"
            for state in ["nu", "ng", "ps"]:
                inist_path=three_path_dict[state]
                for file in os.listdir(inist_path):
                    if not "slurm" in file:
                        continue
                    print(f'Opening file: {inist_path}/{file}')
                    f = open(inist_path + f"/{file}","r",encoding="utf-8")
                    lines = f.readlines()
                    lines.reverse()
                    f.close()
                    for li in lines:
                        if "FINAL SINGLE POINT ENERGY" in li:
                            print(lines.index(li))
                            try:
                                Energy = float(li.split()[4])*27.2113863
                            except:
                                continue
                            r_dict[f"initial_{state}_energy"]=Energy
                            break
            #Ionization and Electron Attachment
            Ionization_Energy=r_dict["initial_ps_energy"]-r_dict["initial_nu_energy"]
            Electron_Attachment_Energy=r_dict["initial_ng_energy"]-r_dict["initial_nu_energy"]
            r_dict["Ionization_Energy"]=Ionization_Energy
            r_dict["Electron_Attachment_Energy"]=Electron_Attachment_Energy

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
    # excel_name = f"Less_than_zero.xls"
    # wb = xlwt.Workbook(encoding="ascii")
    # wsheet = wb.add_sheet("Sheet1")
    # i = 0
    # for key, value in Less_than_zero.items():
    #     wsheet.write(0, i, key)
    #     wsheet.write(1, i, value)
    #     i += 1
    # if not os.path.exists(OUTPUT_PATH):
    #     os.mkdir(OUTPUT_PATH)
    # wb.save(f"{OUTPUT_PATH}/{excel_name}")
    #json plus
    new_data={}
    for x in whole_dict.keys():
        new_value={}
        splits= {}
        for y in whole_dict[x].keys():
            if not y in ["atom_num","atom_ele","formula","initial_nu_energy","initial_ng_energy","initial_ps_energy",
                         "Ionization_Energy","Electron_Attachment_Energy"]:
                splits[y]=whole_dict[x][y]
            else:
                new_value[y]=whole_dict[x][y]
        k=0;temp={};splits_=[]
        for z in splits.keys():
            temp[z]=splits[z]
            k+=1
            if  k==2:
                splits_.append(copy.deepcopy(temp))
                k=0;temp={}
        new_value["splits"]=splits_
        new_data[x]=new_value

    #Save json
    data_file=open("./data.json","w",encoding="utf-8")
    json.dump(new_data,data_file)
    print("json data saved.")
