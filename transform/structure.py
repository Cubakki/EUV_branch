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
    #出于可用性和性能开销的考虑，高频使用的距离矩阵、符号集等对象没有以@property或函数的形式描述，而是作为初始化的一部分完成
    #这意味着 对分子结构的任何直接改动都不会同步至如原子表、符号集、距离矩阵等对象中 ,如需要改变分子结构应创建一个新的molecule实例
    def __init__(self,*args):
        try:
            super().__init__(args[0],args[1],args[2],args[3])
        except:
            raise('Molecule Object Initial Error')
        finally:
            self.__sites__()
            self.__symbol_set__()
            self.__distance_matrix__()
            self.__sites_name_list__()
            self.site_num=len(self.sites)
    def from_structure(self,s : Structure):
        return Molecule(s.name,s.atom_num,s.atom_list,s.coordinate)

    def to_structure(self):
        return Structure(self.name,self.atom_num,self.atom_list,self.coordinate)

    def __distance_matrix__(self):
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
        self.distance_matrix=dm
        return 0

    def __symbol_set__(self):
        ss=[]
        for atom in self.atom_list:
            if not atom in ss:
                ss.append(atom)
        self.symbol_set=ss
        return 0

    def __sites__(self):
        self.sites=[Site(self.atom_list[i],self.coordinate[i],i) for i in range(0,len(self.atom_list))]
        return 0

    def __sites_name_list__(self):
        exist_element = {x: 1 for x in self.symbol_set}
        self.sites_name_list=[]
        self.name2id={}
        for site in self.sites:
            name=site.specie.name + str(exist_element[site.specie.name])
            self.sites_name_list.append(name)
            site.site_name=name
            self.name2id[name]=site.site_id
            exist_element[site.specie.name] += 1
        return 0
    def name2site(self,name):
        '''

        :param name:
        :return: corresponding site
        '''
        return self.sites[self.name2id[name]]

    def get_site(self,site_id):
        return self.sites[site_id]

class Site():
    '''
    molecule实例中的“原子（点）”
    '''

    def __init__(self,specie,coordinate,id=None):
        self.specie=Specie(specie)
        self.coordinate=coordinate
        self.bonded_site=[]    #在molecule中与之成键的site_id
        self.site_id=id     #在molecule中生成sites时初始化
        self.site_name=None    #在molecule中生成site_name_list时初始化

    def add_bond(self,another_site_id):
        self.bonded_site.append(another_site_id)

class Specie():
    '''
    族，即元素类
    '''
    def __init__(self,element):
        self.source_data=Pt.get_element_inf(element)
        self.name=element