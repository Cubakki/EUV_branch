#电离能分析
from load import *
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")

def ionization_list_extract(data_dict):
    ionization=[]
    for stru in data_dict:
        ionization.append(data_dict[stru]["Ionization_Energy"])
    return ionization

def ionization_strusize_lists_extract(data_dict):
    ionization = []
    size = []
    for stru in data_dict:
        ionization.append(data_dict[stru]["Ionization_Energy"])
        size.append(data_dict[stru]["atom_num"])
    return ionization,size


if __name__=="__main__":
    # #总体分布
    # data_dict = load_data()
    # ionization_list=ionization_list_extract(data_dict)
    # sns.displot(data=ionization_list, kde=True, rug=True, color="lightcoral")
    # plt.show()
    #电离能-结构大小散点图
    data_dict = load_data()
    ionization_list ,size_list=ionization_strusize_lists_extract(data_dict)
    ionization_size_array=np.array([size_list,ionization_list])
    sns.jointplot(x=size_list,y=ionization_list,color="lightcoral")
    plt.show()
    pass
