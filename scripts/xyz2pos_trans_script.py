import os
from transform.read import structrue_reader
from transform.poscar_writer import poscar_

if __name__=="__main__":
    read_path= "../resources/SnCHO_f_xyz"
    files=os.listdir(read_path)
    for file in files:
        corrected_name=file.split("SnCHO")[0]
        aimed_path="./resources/POSCAR_SnCHO_First/"+corrected_name
        file_path=read_path+"/"+file
        reader=structrue_reader(file_path)
        writer=poscar_(reader.read(),corrected_name)
        writer.write(aimed_path)