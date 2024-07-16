from pathlib import Path
import json

# Loads element data from json file
with open(str(Path(__file__).absolute().parent / "periodic_table.json"),encoding="utf-8") as f:
    _pt_data = json.load(f)
    f.close()

with open(str(Path(__file__).absolute().parent / "periodic_table_extend1.json"),encoding="utf-8") as f:
    _pt_extend1_data = json.load(f)
    f.close()

class Periodic_table:
    H = "H"
    He = "He"
    Li = "Li"
    Be = "Be"
    B = "B"
    C = "C"
    N = "N"
    O = "O"
    F = "F"
    Ne = "Ne"
    Na = "Na"
    Mg = "Mg"
    Al = "Al"
    Si = "Si"
    P = "P"
    S = "S"
    Cl = "Cl"
    Ar = "Ar"
    K = "K"
    Ca = "Ca"
    Sc = "Sc"
    Ti = "Ti"
    V = "V"
    Cr = "Cr"
    Mn = "Mn"
    Fe = "Fe"
    Co = "Co"
    Ni = "Ni"
    Cu = "Cu"
    Zn = "Zn"
    Ga = "Ga"
    Ge = "Ge"
    As = "As"
    Se = "Se"
    Br = "Br"
    Kr = "Kr"
    Rb = "Rb"
    Sr = "Sr"
    Y = "Y"
    Zr = "Zr"
    Nb = "Nb"
    Mo = "Mo"
    Tc = "Tc"
    Ru = "Ru"
    Rh = "Rh"
    Pd = "Pd"
    Ag = "Ag"
    Cd = "Cd"
    In = "In"
    Sn = "Sn"
    Sb = "Sb"
    Te = "Te"
    I = "I"
    Xe = "Xe"
    Cs = "Cs"
    Ba = "Ba"
    La = "La"
    Ce = "Ce"
    Pr = "Pr"
    Nd = "Nd"
    Pm = "Pm"
    Sm = "Sm"
    Eu = "Eu"
    Gd = "Gd"
    Tb = "Tb"
    Dy = "Dy"
    Ho = "Ho"
    Er = "Er"
    Tm = "Tm"
    Yb = "Yb"
    Lu = "Lu"
    Hf = "Hf"
    Ta = "Ta"
    W = "W"
    Re = "Re"
    Os = "Os"
    Ir = "Ir"
    Pt = "Pt"
    Au = "Au"
    Hg = "Hg"
    Tl = "Tl"
    Pb = "Pb"
    Bi = "Bi"
    Po = "Po"
    At = "At"
    Rn = "Rn"
    Fr = "Fr"
    Ra = "Ra"
    Ac = "Ac"
    Th = "Th"
    Pa = "Pa"
    U = "U"
    Np = "Np"
    Pu = "Pu"
    Am = "Am"
    Cm = "Cm"
    Bk = "Bk"
    Cf = "Cf"
    Es = "Es"
    Fm = "Fm"
    Md = "Md"
    No = "No"
    Lr = "Lr"
    Rf = "Rf"
    Db = "Db"
    Sg = "Sg"
    Bh = "Bh"
    Hs = "Hs"
    Mt = "Mt"
    Ds = "Ds"
    Rg = "Rg"
    Cn = "Cn"
    Nh = "Nh"
    Fl = "Fl"
    Mc = "Mc"
    Lv = "Lv"
    Ts = "Ts"
    Og = "Og"
    def __init__(self):
        self.source_table=_pt_data
        self.extend1_table = _pt_extend1_data
        self.__zt__()

    def __zt__(self):
        self._zt={x:self.source_table[x]["Atomic no"] for x in self.source_table.keys()}

    def get_element_inf(self,ele):
        return self.source_table[ele]

    @property
    def z_table(self):
        #atomic number table for private wrap example: {"H":1}
        return self._zt

    def get_z(self,element_name):
        try:
            return self._zt[element_name]
        except:
            raise TypeError("Illegel element name:{}".format(element_name))

    def get_valence_electron_num(self,element_name):
        try:
            return self.extend1_table["elements"][self._zt[element_name]]["shells"][-1]
        except:
            raise TypeError("Illegel element name:{}".format(element_name))




Pt=Periodic_table()
if __name__=="__main__":
    pt=Periodic_table()

