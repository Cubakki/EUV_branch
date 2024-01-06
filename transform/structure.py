import copy
from periodic_table.periodic_table import Pt

class Structure():
    def __init__(self,name,atom_num,atom_list,coordinate):
        self.name=name
        self.atom_num=atom_num
        self.atom_list=atom_list
        self.coordinate=coordinate #[(x1,y1,z1),(x2,y2,z2),...],cartesian

    def __add__(self, other):
        name=self.name+"_"+other.name
        atom_num=self.atom_num+other.atom_num
        atom_list=self.atom_list+other.atom_list
        coordinate=self.coordinate+other.coordinate
        return Structure(name, atom_num, atom_list, coordinate)


class Molecule(Structure):
    def __init__(self,*args):
        try:
            super().__init__(args[0],args[1],args[2],args[3])
        except:
            pass
    def from_structure(self,s : Structure):
        return Molecule(s.name,s.atom_num,s.atom_list,s.coordinate)

    @property
    def distance_matrix(self):
        dm=[]
        for atom1 in self.coordinate:
            line=[]
            for atom2 in self.coordinate:
                line.append(
                    float(
                            (
                            (atom1[0]-atom2[0])**2
                            +(atom1[1]-atom2[1])**2
                            +(atom1[2]-atom2[2])**2
                            )
                        **0.5
                    )
                )
            dm.append(copy.deepcopy(line))
        return dm

    @property
    def symbol_set(self):
        ss=[]
        for atom in self.atom_list:
            if not atom in ss:
                ss.append(atom)
        return ss

    @property
    def sites(self):
        return [Site(self.atom_list[i],self.coordinate[i]) for i in range(0,len(self.atom_list))]
        pass

class Site():
    '''
    molecule实例中的“原子（点）”
    '''

    def __init__(self,specie,coordinate):
        self.specie=Specie(specie)
        self.coordinate=coordinate

class Specie():
    '''
    族，即元素类
    '''
    def __init__(self,element):
        self.source_data=Pt.get_element_inf(element)
        self.name=element



a=Structure('A',5,['H','H','H','H','H'],[(0,0,0),(1,1,1),(2,2,2),(3,3,3),(4,4,4)])
m=Molecule().from_structure(a)
print(m.distance_matrix)
print(m.sites)
print(1)