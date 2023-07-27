#电子亲合能分析
from load import *
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")

def attachment_list_extract(data_dict):
    attachment=[]
    for stru in data_dict:
        attachment.append(data_dict[stru]["Electron_Attachment_Energy"])
    return attachment

def attachment_strusize_lists_extract(data_dict):
    attachment = []
    size = []
    for stru in data_dict:
        attachment.append(data_dict[stru]["Electron_Attachment_Energy"])
        size.append(data_dict[stru]["atom_num"])
    return attachment,size


if __name__=="__main__":
    # #总体分布
    # data_dict = load_data()
    # attachment_list=attachment_list_extract(data_dict)
    # sns.displot(data=attachment_list, kde=True, rug=True, color="skyblue")
    # plt.show()
    #电离能-结构大小散点图
    data_dict = load_data()
    attachment_list ,size_list=attachment_strusize_lists_extract(data_dict)
    attachment_size_array=np.array([size_list,attachment_list])
    sns.jointplot(x=size_list,y=attachment_list,color="skyblue")
    plt.show()
    pass