from transform.structure import Structure


class Structrue_reader:
    def __init__(self):
        self.alive =True

    def read(self,path,type=None):
        self.type = type
        self.path = path
        if self.type == None:
            self.type = self.type_judge(path)
        f = open(path, "r")
        self.line_list = [x.strip() for x in f.readlines()]
        f.close()
        return self.type_assign()

    def type_judge(self,path):
        try:
            type=path.split(".")[-1]
        except:
            print("File type judge error:{}".format(path))
            raise TypeError
        return type

    def type_assign(self):
        if self.type=="xyz":
            return(self.xyz_reader())
        #elif self.type=="cif":
            #return (self.cif_reader())
        else:
            print("Unsupport Type Error:{}".format(self.type))
            raise TypeError


    def xyz_reader(self):
        self.name=self.line_list[1]
        self.atom_num=int(self.line_list[0])
        self.atom_list=[];self.coordinate=[]
        for line in self.line_list[2:]:
            line=line.strip()
            tup=line.split()
            self.atom_list.append(tup[0])
            self.coordinate.append(tuple([float(x) for x in tup[1:]]))
        return Structure(self.name,self.atom_num,self.atom_list,self.coordinate)

structure_reader=Structrue_reader()