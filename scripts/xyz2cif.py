import os.path

from transform.structure import Structure
from transform.read import Structrue_reader
from transform.cif_writer import cif_


RPath=[]
def recursion_dir(pre_path):
    #report xyz files in global list 'RPath'
    global RPath
    if not os.path.isdir(pre_path):
        if os.path.basename(pre_path).split(".")[-1]=="xyz":
            RPath.append(pre_path)
    else:
        secs=os.listdir(pre_path)
        for sec in secs:
            sec_path=os.path.join(pre_path,sec)
            recursion_dir(sec_path)

if __name__=="__main__":
    root="./to_cif/structure_data"
    recursion_dir(root);i=0
    for p in RPath:
        np="."+p.split(".")[1]+".cif"
        sr=Structrue_reader()
        st=sr.read(p)
        cr=cif_(st)
        cr.write(np)
        i+=1
    print('Done : {} items'.format(i))