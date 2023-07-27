

class structure():
    def __init__(self,name,atom_num,atom_list,coordinate):
        self.name=name
        self.atom_num=atom_num
        self.atom_list=atom_list
        self.coordinate=coordinate

    def __add__(self, other):
        name=self.name+"_"+other.name
        atom_num=self.atom_num+other.atom_num
        atom_list=self.atom_list+other.atom_list
        coordinate=self.coordinate+other.coordinate
        return structure(name,atom_num,atom_list,coordinate)