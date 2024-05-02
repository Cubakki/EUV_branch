#Sn-C键解离能分析
#VOCYEN和YAMFUN
from load import *
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")

def dissociation_list_extract(data_dict):
    dissociation=[]
    corresponding_key=[]
    less_than_zero={}
    less_than_zero_addinfo={}
    for stru in data_dict:
        for keyname in data_dict[stru]:
            if "split" in keyname:
                dso=float(format(data_dict[stru][keyname],".3f"))
                if dso<1 and "H" in data_dict[stru]["atom_ele"]:# and (("ps" in keyname) or ("ng" in keyname)):
                    print(f"{stru}_{keyname}:{dso}")
                    if not stru in less_than_zero.keys():
                        less_than_zero[stru]=[{keyname:dso}]
                        less_than_zero_addinfo[stru]=[{"Ionization_Energy":data_dict[stru]["Ionization_Energy"],
                                                       "Electron_Attachment_Energy":data_dict[stru]["Electron_Attachment_Energy"]}]
                    else:
                        less_than_zero[stru].append({keyname:dso})
                if stru == "Sn12Cluster":
                    dissociation.append(dso)
                    corresponding_key.append([keyname])
                    continue
                if  dso<30.0 and dso >0:
                    dissociation.append(dso)
                    corresponding_key.append([keyname])
                else:
                    #print(f"\n{keyname}:{dso},so high !!!!")
                    pass
    #end loop
    print(less_than_zero)
    return dissociation


if __name__=="__main__":
    #总体分布
    data_dict = load_data()
    dissociation_list=dissociation_list_extract(data_dict)

    sns.despine(top=True, right=True)
    sns.displot(data=dissociation_list, kde=True, rug=True, color="turquoise")
    plt.show()
    pass