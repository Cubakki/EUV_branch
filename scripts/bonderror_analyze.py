import os
import shutil


def load_folderflist(folder):
    f_list=os.listdir(folder)
    return f_list

class mol_loader():
    def __init__(self):
        self.name=None
        self.atom_num : int
        self.bond_num : int
        '''
        以下列表序号对应
        '''
        self.atom_list=[]
        self.pos_list=[]
        self.bond_num_list=[]  #键数
        self.bond_list=[]  #键，对应序数上是成键原子列表
        self.bondlevel_list=[]
        '''
        以上列表序号对应
        '''
        pass

    def read(self,fpath):
        f=open(fpath,"r")
        fl=f.readlines()
        f.close()
        self.name=fl[0].strip()
        self.other=fl[1:4]
        self.atom_num=int(fl[3][:3].strip())
        self.bond_num_list=[0 for x in range(0,self.atom_num)]
        self.bond_list=[[] for x in range(0,self.atom_num)]
        self.bondlevel_list=[[] for x in range(0,self.atom_num)]
        self.bond_num=int(fl[3][3:6].strip())
        atom_part=fl[4:4+self.atom_num]
        bond_part=fl[4+self.atom_num:4+self.atom_num+self.bond_num]
        for atom in atom_part:
            posx,posy,posz=float(atom[0:10].strip()),float(atom[10:20].strip()),float(atom[20:30].strip())
            element=atom[30:34].strip()
            self.pos_list.append((posx,posy,posz))
            self.atom_list.append(element)
        for bond in bond_part:
            a=int(bond[0:3].strip())
            b=int(bond[3:6].strip())
            level=int(bond[6:9].strip())
            self.bond_num_list[a-1]+=1
            self.bond_num_list[b-1]+=1
            self.bond_list[a-1].append(b)
            self.bond_list[b-1].append(a)
            self.bondlevel_list[a-1].append(level)
            self.bondlevel_list[b-1].append(level)

    def show_bond_num(self):
        ret=None
        for i in range(0,self.atom_num):
            #print("元素:{},键数:{}".format(self.atom_list[i],self.bond_num_list[i]))
            if self.atom_list[i]=="C":
                if self.bond_num_list[i]>4:
                    print("在{}中，存在C连接了{}个键".format(self.name,self.bond_num_list[i]))
                    ret=self.name
        return ret


def execlusive(pre,tic):
    if not tic==None:
        print(tic)
        pre.append(tic)
    return pre


if __name__=="__main__":
    load_dir="../resources/old/SnCHO/mol_tem"
    # shutil_dir="../resources/old/SnCHO_xyz"
    # paste_dir="../resources/SnCHO_flitered"
    # if not os.path.exists(paste_dir):
    #     os.mkdir(paste_dir)
    file_list=load_folderflist(load_dir)
    # exec=[]
    for file in file_list:
        a=mol_loader()
        a.read("{}/{}".format(load_dir,file))
        tic=a.show_bond_num()
    #     exec=execlusive(exec,tic)
    # print(exec)
    #
    # for file in file_list:
    #     if not file.split("SnCHO")[0] in exec:
    #         shutil.copy(shutil_dir+"/{}".format(file.replace("mol","xyz")),paste_dir+"/{}".format(file.split("SnCHO")[0]+".xyz"))
