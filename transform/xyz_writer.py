from transform.structure import Structure

class xyz_:
    def __init__(self, structure : Structure, name = None):
        self.structure=structure
        if name==None:
            self.name=self.structure.name

    def pre_cal(self):
        self.atom_dict={}
        for atom in self.structure.atom_list:
            if atom in self.atom_dict.keys():
                self.atom_dict[atom]+=1
            else:
                self.atom_dict[atom] =1
        return True

    def write(self,output_filepath,tip=""):
        head=f"{self.structure.atom_num}"
        type_num=[]
        for atom in self.atom_dict.keys():
            type_num.append("{}{}".format(atom,self.atom_dict[atom]))
        tip =tip+"{}".format(" ".join(type_num))
        coor_list=[]
        for i in range(0,self.structure.atom_num):
            coor_list.append("{} {:.4f} {:.4f} {:.4f}".format(self.structure.atom_list[i],
                                                  self.structure.coordinate[i][0],
                                                  self.structure.coordinate[i][1],
                                                  self.structure.coordinate[i][2]))
        coor="\n".join(coor_list)
        content="{}\n" \
                "{}\n" \
                "{}".format(head,tip,coor)
        with open(output_filepath,"w")as f:
            f.write(content)
            f.close()
