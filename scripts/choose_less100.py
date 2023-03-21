import os
import shutil

def choose():
    directory="./SnCHO_xyz"
    output_d="./target"
    if not os.path.exists(output_d):
        os.mkdir(output_d)
    qualified_num=0
    for file in os.listdir(directory):
        f=open(f"./{directory}/{file}",'r')
        atom_num=int(f.readlines()[0])
        f.close()
        if atom_num<30:
            #name=".".join(".SnCHO".join(file.split("SnCHO")).split(".")[:-1])+".cif"
            name=f"./{directory}/{file}"
            shutil.copy(name,output_d)
            #shutil.copy(f"./SnCHO/{name}",output_d)
            print("符合要求的文件{}".format(name))
            qualified_num+=1
    print("共有{}个文件符合要求".format(qualified_num))

if __name__=="__main__":
    choose()