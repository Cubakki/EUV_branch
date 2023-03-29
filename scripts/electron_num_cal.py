from pymatgen.core import Molecule

def calculate_electron_num(xyz_file_path):
    molecule = Molecule.from_file(xyz_file_path)
    ele_num=0
    for index in range(0,molecule.num_sites):
        ele_num+=molecule.sites[index].specie.number
    print("此结构的电子数:\n{}".format(ele_num))


if __name__=="__main__":
    calculate_electron_num("../Sn12/Sn12.xyz")