import json
from typing import Dict,List

def load_data(fp="./data.json") -> Dict:
    with open(fp,"r") as f:
        data=json.load(f)
        f.close()
    return data

def load_split(data_dict):
    #Some structures are not legal to be split
    splitstru_list=[]
    for stru in list(data_dict.keys()):
        split=False
        for key_name in list(data_dict[stru].keys()):
            if "split" in key_name:
                split=True
        if split==True:
            splitstru_list.append(stru)
    return splitstru_list

if __name__=="__main__":
    data_dict=load_data()
    split_list=load_split(data_dict)
    i=0
    for stru in split_list:
        data=data_dict[stru]
        for kn in list(data.keys()):
            if "split" in kn:
                i+=1
    print(i)
    pass