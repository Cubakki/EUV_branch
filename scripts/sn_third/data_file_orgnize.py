import os
import copy
import shutil
import json

if __name__=="__main__":

    with open("./data_.json","r") as f:
        data : dict =json.load(f)
        f.close()

    initial_path="./workdir"
    orgnize_path="./structure_data"

    if not os.path.exists(orgnize_path):
        os.mkdir(orgnize_path)

    #shutil.copy("./data_.json",os.path.join(orgnize_path,"data_.json"))

    for sname in  data.keys():
        isp=initial_path+f"/{sname}"
        op=orgnize_path+f"/{sname}"
        if not os.path.exists(op):
            os.mkdir(op)
        svalue=data[sname]
        spath=initial_path+f"/{sname}"
        shutil.copy(spath+"/nu.xyz",op)
        shutil.copy(spath+"/ng.xyz",op)
        shutil.copy(spath+"/ps.xyz",op)
        svalue["initial_nu_energy"] = [copy.deepcopy(svalue["initial_nu_energy"]), op + "/nu.xyz"]
        svalue["initial_ng_energy"] = [copy.deepcopy(svalue["initial_ng_energy"]), op + "/ng.xyz"]
        svalue["initial_ps_energy"] = [copy.deepcopy(svalue["initial_ps_energy"]), op + "/ps.xyz"]

        if not svalue["splits"]==[]:
            for pairs in svalue["splits"]:
                tag=list(pairs.keys())[0]
                tag_= "_".join(tag.split("_")[:-1])
                subpath="/".join(tag.split("_")[:-2])
                wsp=os.path.join(isp,subpath)
                corep=os.path.join(wsp,"core.xyz")
                ligandp=os.path.join(wsp,"ligand.xyz")
                pairs["paths"]=[op+f"/{tag_}_core.xyz",op+f"/{tag_}_ligand.xyz"]
                if not os.path.exists(op+f"/{tag_}_core.xyz"):
                    shutil.copy(corep,op+f"/{tag_}_core.xyz")
                if not os.path.exists(op+f"/{tag_}_ligand.xyz"):
                    shutil.copy(ligandp,op+f"/{tag_}_ligand.xyz")

    with open("data_orgnized.json","w") as f:
        text=json.dumps(data)
        f.write(text)
        f.close()









































    '''
    change initial data.json to a better form
    '''
    # with open("./data.json","r") as f:
    #     data : dict =json.load(f)
    #     f.close()
    #
    # new_data={}
    # for x in data.keys():
    #     new_value={}
    #     splits= {}
    #     for y in data[x].keys():
    #         if not y in ["atom_num","atom_ele","initial_nu_energy","initial_ng_energy","initial_ps_energy",
    #                      "Ionization_Energy","Electron_Attachment_Energy"]:
    #             splits[y]=data[x][y]
    #         else:
    #             new_value[y]=data[x][y]
    #     k=0;temp={};splits_=[]
    #     for z in splits.keys():
    #         temp[z]=splits[z]
    #         k+=1
    #         if  k==2:
    #             splits_.append(copy.deepcopy(temp))
    #             k=0;temp={}
    #     new_value["splits"]=splits_
    #     new_data[x]=new_value
    #
    # with open("data_.json","w") as f:
    #     text=json.dumps(new_data)
    #     f.write(text)
    #     f.close()