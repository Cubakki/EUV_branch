from transform.structure import Structure


'''
由于VASP需要固定的元素顺序（方便POTCAR赝势的统一），目前支持的是Sn、O、C、H的排列
'''
class poscar_:
    def __init__(self, structure : Structure, name=None):
        self.structure=structure
        if not name==None:
            self.structure.name=name
        self.pre_cal()

    def pre_cal(self):
        self.ele_pos_dict={}
        for i in range(0,len(self.structure.atom_list)):
            if self.structure.atom_list[i] not in self.ele_pos_dict.keys():
                self.ele_pos_dict[self.structure.atom_list[i]]=[self.structure.coordinate[i]]
            else:
                self.ele_pos_dict[self.structure.atom_list[i]].append(self.structure.coordinate[i])
        return True


    def first_line(self):
        return self.structure.name

    def multiply_power(self):
        #晶格矢量倍率因子
        return "1.0"

    def vector(self):
        #晶格矢量，是3x3的矩阵，输出为str格式
        xl,yl,zl=[],[],[]
        for coords in self.structure.coordinate:
            xl.append(coords[0]);yl.append(coords[1]);zl.append(coords[2])
        x_=(max(xl)-min(xl))+10
        y_=(max(yl)-min(yl))+10
        z_=(max(zl)-min(zl))+10
        vector="{:.9f}   0.000000000   0.000000000\n" \
               "0.000000000   {:.9f}   0.000000000\n" \
               "0.000000000   0.000000000   {:.9f}".format(x_,y_,z_)
        return vector

    def element_part(self):
        '''
        元素列
        :return:
        “
        ElementA  ElementB  ElementC  ...
        numA      numB      numC
        ”
        '''
        '''
        ele_num_pair=[]
        for ele in list(self.ele_pos_dict.keys()):
                ele_num_pair.append(tuple([ele,len(self.ele_pos_dict[ele])]))
        line_one="   ".join([x[0] for x in ele_num_pair])
        line_two="  ".join([x[1] for x in ele_num_pair])
        element_part_str=line_one+"\n"\
                        +line_two
        self.ele_part_arrange=list([x[0] for x in ele_num_pair])
        return element_part_str
        '''
        #以上为正常版，可以配合生成POTCAR文件
        #以下为暂行版，适应于目前使用的Sn、O、C、H，方便使用固定的POTCAR文件

        self.ele_part_arrange=["Sn","O","C","H"]
        line_one="   ".join(["Sn","O","C","H"])
        line_two="  ".join([str(len(self.ele_pos_dict[x])) for x in ["Sn","O","C","H"]])
        element_part_str=line_one+"\n"\
                        +line_two
        return element_part_str


    def coordinate_part(self):
        type="Cartesian\n"
        body=""
        for ele in self.ele_part_arrange:
            for coor in self.ele_pos_dict[ele]:
                body+="{:.9f}  {:.9f}  {:.9f}\n".format(coor[0],coor[1],coor[2])
        coordinate_part_str=type+body
        return coordinate_part_str

    def write(self,output_file_path):
        text=self.first_line()+"\n"\
            +self.multiply_power()+"\n"\
            +self.vector()+"\n"\
            +self.element_part()+"\n"\
            +self.coordinate_part()
        f=open(output_file_path,"w")
        f.write(text)
        f.close()
        print("成功生成{}".format(output_file_path))
