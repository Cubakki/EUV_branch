from transform.read import structure_reader
from transform.openmx_input_writer import OpenMXInputWriter
import os

structure_path = "./structures"
work_path = "./openmx_workdir"
DFT_DATA_PATH = "/public/spst/home/wanghan3_6/softwares/openmx3.9/DFT_DATA19/"

if __name__ == '__main__':

    ################################ check if there is a work log
    if not os.path.exists("./worked.log"):
        with open("./worked.log", 'w') as f:
            f.close()
    ################################ load worked structure
    with open("./worked.log", "r", encoding="utf-8") as fr:
        worked = fr.readlines()
        fr.close()
        worked = [x.strip() for x in worked]
    ################################

    worklist = []
    for struct_file in os.listdir(structure_path):
        if not struct_file.split(".")[0] in worked:
            struct = struct_file.split(".")[0]
            stuct_file_path = structure_path + "/" + struct_file
            struct_work_path = work_path + "/" + struct  +"/"
            if not os.path.exists(struct_work_path):
                os.makedirs(work_path + "/" + struct)
            structure = structure_reader.read(stuct_file_path)
            ome = OpenMXInputWriter(structure)
            ome.data_path(DFT_DATA_PATH)
            ome.write_openmx_input_file(struct_work_path)
            worklist.append(struct)



    ################################
    with open("./worklist","w", encoding="utf-8") as fw:
        fw.write("\n".join(worklist))
        fw.close()
    ################################