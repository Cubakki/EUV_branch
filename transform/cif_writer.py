#  structure -->　cif file   !!!! 仅做简单格式适配，保证格矢大于格点体积，cell angle都为90°，a/b/c lenth取在此方向最远投影点间距离的两倍
import copy

from transform.structure import structure

class cif_():
    def __init__(self, structure: structure, name=None):
        self.structure = structure
        if name == None:
            self.name = self.structure.name

        #just be used to hint
        self.template = 'data_global\n' \
                        '_chemical_name \'New material\'\n' \
                        '_cell_length_a 1.0\n'\
                        '_cell_length_b 1.0\n'\
                        '_cell_length_c 1.0\n'\
                        '_cell_angle_alpha 90\n'\
                        '_cell_angle_beta 90\n'\
                        '_cell_angle_gamma 90\n'\
                        '_symmetry_space_group_name_H-M \'P 1\'\n'\
                        'loop_\n'\
                        '_atom_site_label\n'\
                        '_atom_site_fract_x\n'\
                        '_atom_site_fract_y\n'\
                        '_atom_site_fract_z\n'\
                        'H 0 0 0'
        #
        self.key_list=["data_global","_cell_length_a","_cell_length_b","_cell_length_c","_cell_angle_alpha",
                       "_cell_angle_beta","_cell_angle_gamma","_symmetry_space_group_name_H-M","loop_",
                       "_atom_site_label","_atom_site_fract_x","_atom_site_fract_y","_atom_site_fract_z"]
        #Every line will be transferd as a key value pair to save in this dict.
        #Finally, we join every key value pair with an ' ' to ge a single line.
        self.global_section={"_cell_length_a":"","_cell_length_b":"","_cell_length_c":"",
                             "_cell_angle_alpha":"","_cell_angle_beta":"","_cell_angle_gamma":"",
                             "_symmetry_space_group_name_H-M":""}
        self.symmetry_equiv_pos_as_xyz_loop = ["loop_", "_symmetry_equiv_pos_as_xyz", "x,y,z"]
        self.atom_site_loop=["loop_","_atom_site_label","_atom_site_fract_x","_atom_site_fract_y","_atom_site_fract_z"]

        self.fill_information()

    def fill_information(self):
        #global data
        xl, yl, zl = [], [], []
        for coords in self.structure.coordinate:
            xl.append(coords[0]);yl.append(coords[1]);zl.append(coords[2])
        x_=(max(xl)-min(xl))+10
        y_=(max(yl)-min(yl))+10
        z_=(max(zl)-min(zl))+10
        #为每个基规定一个分数最小值，用实际分数坐标减去此值以使所有坐标为正
        xm_=min(xl)/x_
        ym_=min(yl)/y_
        zm_=min(zl)/z_
        #fill global data
        global_fill_list=[x_,y_,z_,90,90,90,'P 1']
        for i in range(0,7):
            self.global_section[list(self.global_section.keys())[i]]=copy.deepcopy(global_fill_list[i])

        #atom_site_loop
        for i in range(0, self.structure.atom_num):
            self.atom_site_loop.append("{} {:.4f} {:.4f} {:.4f}".format(self.structure.atom_list[i],
                                                                        (self.structure.coordinate[i][0]+5)/x_-xm_,
                                                                        (self.structure.coordinate[i][1]+5)/y_-ym_,
                                                                        (self.structure.coordinate[i][2]+5)/z_-zm_))
        pass
    def write(self,output_path):
        #组装str
        output=['data_global','_chemical_name \'{}\''.format(self.name)]
        #global_add
        for key in self.global_section.keys():
            output.append(key+' '+str(self.global_section[key]))
        # symmetry_xyz_add
        for item in self.symmetry_equiv_pos_as_xyz_loop:
            output.append(item)
        #atom_site_add
        for item in self.atom_site_loop:
            output.append(item)

        output_str="\n".join(output)

        with open(output_path,"w") as f:
            f.write(output_str)
            f.close()
        print('succeed to write {}'.format(output_path))