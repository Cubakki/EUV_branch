#分析已计算结构的大小组成
from load import *
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")

if __name__=="__main__":
    data_dict=load_data()
    atom_num_list=[]
    for stru in data_dict.keys():
        atom_num=data_dict[stru]["atom_num"]
        atom_num_list.append(atom_num)

    print(atom_num_list)
    delta=max(atom_num_list)-min(atom_num_list)
    slices=delta//10+1
    an_array=np.array(atom_num_list)
    sns.displot(data=an_array,bins=slices,kde=True,rug=True,color="palevioletred")
    plt.show()