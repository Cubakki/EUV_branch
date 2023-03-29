import copy
import os
import numpy as np

#本脚本将读取并改变一对core-ligand的键长，按一定间隔输出为一系列xyz文件，供势能面计算使用
#为方便程序结构与运行，已将一些reader与structure类移植入本文件
'''
运行本脚本需要输入3个文件，分别为:
1、核(core)的xyz文件
2、配体(ligand)的xyz文件
3、连接核与配体的键文件，不做后缀名要求，包含键两侧原子的位置信息，信息格式与xyz文件中相同
***三者均应由同一结构文件生成，即二者拼合按坐标排列时可以重构为原结构

需要指定一个输出路径(文件夹)，输出文件为一系列xyz文件，分别以核-配体的键长命名。可以指定一个名字，使它在键长之前出现。
'''

class PES_sg():
    def __init__(self,core_f,ligand_f,bond_f,out_path):
        sr=structrue_reader()
        self.core=sr.read(core_f);self.ligand=sr.read(ligand_f)
        self.bondf=open(bond_f,"r").readlines()
        self.outpath=out_path
        if not os.path.exists(out_path):
            os.mkdir(self.outpath)
        self.gen_bond_vector()

    def gen_bond_vector(self):
        self.site1, self.site1_coor = self.bondf[0].split()[0], self.bondf[0].split()[1:]
        self.site2, self.site2_coor = self.bondf[1].split()[0], self.bondf[1].split()[1:]
        self.site1_coor = np.array([float(x) for x in self.site1_coor])
        self.site2_coor = np.array([float(x) for x in self.site2_coor])
        self.bond_vector=self.site2_coor-self.site1_coor
        self.bond_norm=self.bond_vector.dot(self.bond_vector)**0.5

    def run(self,internal=0.1,num=50,start=None,first_name=""):
        '''
        变化的键长中值将默认设定为原始键长，间隔与数目可以设定；最小从0.5埃开始输出结构
        :param internal: 间隔，单位为埃
        :param num: 间隔应用的次数（键长变化范围）;num为x时，有x+1个结构被输出
        :return: True
        '''
        internal=float(internal)
        num=int(round(float(num),0))
        mid_point=round(self.bond_norm,1)
        if start==None:
            start=round(mid_point-round((num/2),0)*internal,1)
        if start!=None:
            if start<0.5:
                start=0.5
        for i in range(0,num+1):
            actual_bl=start+i*internal
            #actual_bondlenth
            change_vector=((actual_bl-self.bond_norm)/self.bond_norm)*self.bond_vector
            actual_bl_str=str(round(actual_bl,1)).replace(".","p")
            if not first_name=="":
                name=f"{first_name}_{actual_bl_str}A.xyz"
            else:
                name=f"{actual_bl_str}A.xyz"
        #move ligand
            new_coor=[]
            for coor in self.ligand.coordinate:
                new_coor.append(tuple(np.array(coor)+change_vector))
            new_ligand=copy.deepcopy(self.ligand)
            new_ligand.coordinate=new_coor
            aggregation=self.core+new_ligand
            writer=xyz_writer(aggregation,name)
            writer.write(self.outpath+"/"+name,)


class structrue_reader:
    def __init__(self):
        pass

    def read(self,path,type=None):
        self.type = type
        if self.type == None:
            self.type = self.type_judge(path)
        f = open(path, "r")
        self.line_list = f.readlines()
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
        return structure(self.name,self.atom_num,self.atom_list,self.coordinate)

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

class xyz_writer:
    def __init__(self,structure : structure,name = None):
        self.structure=structure
        if name==None:
            name=self.structure.name
        self.pre_cal()

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