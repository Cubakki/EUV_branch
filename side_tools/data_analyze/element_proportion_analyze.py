#元素比重分布作图
from load import *
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")

def cal_sn_proportion(atom_ele_list):
    sn_num=0
    all_num=len(atom_ele_list)
    for ele in atom_ele_list:
        if ele=="Sn":
            sn_num+=1
    return float(format(sn_num/all_num,".3f"))

def cal_h_c_proportion(atom_ele_list):
    c_num = 0
    h_num = 0
    all_num = len(atom_ele_list)
    for ele in atom_ele_list:
        if ele == "C":
            c_num += 1
        elif ele == "H":
            h_num += 1
    return float(format(h_num / c_num, ".3f"))

def atom_num_list(data_dict):
    size = []
    for stru in data_dict:
        size.append(data_dict[stru]["atom_num"])
    return size

if  __name__=="__main__":
    data_dict = load_data()
    # #Sn_proportion
    #sn_proportion_list=[]
    # for stru_data in list(data_dict.values()):
    #     atom_ele=stru_data["atom_ele"]
    #     sn_proportion_list.append(cal_sn_proportion(atom_ele))
    # sn_proportion_array=np.array(sn_proportion_list)
    # sns.displot(data=sn_proportion_array, kde=True, rug=True, color="plum")
    # plt.show()
    # #h_c_propotion
    # h_c_proportion_list = []
    # for stru_data in list(data_dict.values()):
    #     atom_ele=stru_data["atom_ele"]
    #     h_c_proportion_list.append(cal_h_c_proportion(atom_ele))
    # h_c_proportion_array=np.array(h_c_proportion_list)
    # sns.displot(data=h_c_proportion_array, kde=True, rug=True, color="plum")
    # plt.show()
    #h_c_proportion&size scatter
    h_c_proportion_list = []
    for stru_data in list(data_dict.values()):
        atom_ele = stru_data["atom_ele"]
        h_c_proportion_list.append(cal_h_c_proportion(atom_ele))
    size_list=atom_num_list(data_dict)
    h_c_proportion_array = np.array(h_c_proportion_list)
    sns.displot(data=h_c_proportion_array, kde=True, rug=True, color="plum")
    sns.jointplot(x=size_list, y=h_c_proportion_list, color="plum")
    plt.show()