#Utils
from pymatgen.core import Molecule

def calculate_electron_num(xyz_file_path):
    molecule = Molecule.from_file(xyz_file_path)
    ele_num=0
    for index in range(0,molecule.num_sites):
        ele_num+=molecule.sites[index].specie.number
    #print("此结构的电子数:\n{}".format(ele_num))
    return ele_num

def electron_num_reader(ele_num_txt_path):
    ele_num_f = open(ele_num_txt_path, "r")
    ele_num_both = ele_num_f.readlines()
    core_ele_num=int(ele_num_both[0].split(":")[1])
    ligand_ele_num=int(ele_num_both[1].split(":")[1])
    ele_num = int(ele_num_both[0].split(":")[1]) + int(ele_num_both[1].split(":")[1])
    return [ele_num,core_ele_num,ligand_ele_num]

def PES_pbs_bash(target_dir,pbs_script_name):
    '''
    Generate a bash to cd into the specific directory and execute the pbs_script to submit a pbs task.
    :param target_dir: eg:"./a/b/c"
    :return:
    '''
    bash_text = f"echo \" in bash-->target_dir:{target_dir}\"\n" \
                f"cd {target_dir}\n" \
                f"qsub {pbs_script_name}\n" \
                f"echo \"已执行:qsub {pbs_script_name}\""
    # print(bash_text)
    b_name = f"pbs_activate.sh"
    b_path = f"{target_dir}/{b_name}"
    f = open(target_dir+"/"+b_name, 'w')
    f.write(bash_text)
    f.close()
    return b_path