from typing import Union
import os
'''
ORCA的格式：
-以"#"开头的标题行
-在文件最开头，以"!"开头的关键词行
-以"%"开头，"end"结尾，多行的block
-以"*"开头与结尾的坐标行，包括坐标格式、电荷数、自旋多重度和多行坐标

*这里的blocks包括了核心数等设定
'''

class ORCA_INPUT:

    def __init__(self,key_line : str,structure_file,electron_num = 0,block = None):
        self.keyline=key_line
        self.strfile=structure_file
        self.elenum=electron_num
        self.block=block
        self.coord_deal()

    def coord_deal(self):
        type=os.path.splitext(self.strfile)[-1]
        with open(self.strfile,"r") as f:
            file_content=f.readlines()
            f.close()
        if type == ".xyz":
            self.type="xyz"
            self.xyz_deal(file_content)
        else:
            raise TypeError("不支持的类型")

    def xyz_deal(self,file_content):
        line_list=file_content
        self.name = line_list[1]
        self.atom_num = int(line_list[0])
        self.atom_list = []
        self.coordinate = []
        self.xyz_lines = []
        for line in line_list[2:]:
            tup = line.split()
            self.xyz_lines.append(line)
            self.atom_list.append(tup[0])
            self.coordinate.append(tuple([float(x) for x in tup[1:]]))
        #spin是单、三重态判断，级简单的2S+1，假定α、β电子成对出现
        if (self.elenum%2)==1:
            self.spin=1
        else:
            self.spin=0



    def write(self,write_path):
        content=""
        if not "\n" in self.keyline:
            self.keyline+="\n"
        content+=self.keyline
        if not self.block==None:
            for blo in self.block:
                content=content+blo+"\n"
        coor="* {} {} {}\n".format(self.type,0,self.spin)
        for line in self.xyz_lines:
            line=line.strip()
            coor=coor+line+"\n"
        coor+="*"
        content+=coor
        with open(write_path,"w") as w:
            w.write(content)
            w.close()

if __name__=="__main__":
    keyline="!TPSS D4  DEF2-SVP SP\n"
    block=["% PAL NPROCS 32 END\n","%scf SmearTemp 5000 \nend"]
    orca=ORCA_INPUT(keyline,"./ACDMSNSnCHO_alone.xyz",0,block)
    orca.write("input.inp")