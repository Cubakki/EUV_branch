from _ast import arg

from transform.structure import Structure
from periodic_table.periodic_table import Pt

basis_configuration_dict = {"H"  : ["H5.0-s3p2","H_PBE19"],
                            "He" : ["He8.0-s2p2d1","He_PBE19"],
                            "Li" : ["Li8.0-s3p3d2","Li_PBE19"],
                            "Be" : ["Be7.0-s3p2","Be_PBE19"],
                            "B"  : ["B7.0-s2p2d1","B_PBE19"],
                            "C"  : ["C6.0-s2p2d1","C_PBE19"],
                            "N"  : ["N6.0-s3p3d2","N_PBE19"],
                            "O"  : ["O7.0-s3p3d2","O_PBE19"],
                            "F"  : ["F6.0-s3p3d2","F_PBE19"],
                            "Ne" : ["Ne9.0-s3p3d2","Ne_PBE19"],
                            "Na" : ["Na9.0-s3p3d2","Na_PBE19"],
                            "Mg" : ["Mg7.0-s3p3d2","Mg_PBE19"],
                            "Al" : ["Al7.0-s4p4d2","Al_PBE19"],
                            "Si" : ["Si7.0-s2p2d1","Si_PBE19"],
                            "P"  : ["P7.0-s4p3d3f2","P_PBE19"],
                            "S"  : ["S7.0-s4p3d3f2","S_PBE19"],
                            "Cl" : ["Cl7.0-s3p3d2","Cl_PBE19"],
                            "Ar" : ["Ar9.0-s3p3d2f1","Ar_PBE19"],
                            "K"  : ["K10.0-s4p3d3f1","K_PBE19"],
                            "Ca" : ["C9.0-s4p3d3f1","Ca_PBE19"],
                            "Sc" : ["S7.0-s4p3d3f1","Sc_PBE19"],
                            "Ti" : ["Ti7.0-s3p3d2","Ti_PBE19"],
                            "V"  : ["V6.0-s3p3d2","V_PBE19"],
                            "Cr" : ["Cr6.0-s3p3d2","Cr_PBE19"],
                            "Mn" : ["Mn6.0-s3p3d3","Mn_PBE19"],
                            "Fe" : ["Fe6.0S-s3p3d2","Fe_PBE19S"],
                            "Co" : ["Co6.0S-s2p3d2f1","Co_PBE19S"],
                            "Ni" : ["Ni6.0S-s3p3d2f1","Ni_PBE19S"],
                            "Cu" : ["Cu6.0S-s2p2d2","Cu_PBE19S"],
                            "Zn" : ["Zn6.0S-s2p2d2","Zn_PBE19S"],
                            "Ga" : ["Ga7.0S-s2p2d2","Ga_PBE19"],
                            "Ge" : ["Ge7.0S-s3p3d3f2","Ge_PBE19"],
                            "As" : ["As7.0S-s2p2d2f1","As_PBE19"],
                            "Se" : ["Se7.0S-s3p3d2f1","Se_PBE19"],
                            "Br" : ["Br7.0-s3p2d1","Br_PBE19"],
                            "Kr" : ["Kr10.0-s3p2d2f1","Kr_PBE19"],
                            "Rb" : ["Rb11.0-s3p3d2f2","Rb_PBE19"],
                            "Sr" : ["Sr10.0-s3p2d2f2","Sr_PBE19"],
                            "Y"  : ["Y8.0-s4p3d3f2","Y_PBE19"],
                            "Zr" : ["Zr7.0-s3p2d2","Zr_PBE19"],
                            "Nb" : ["Nb7.0-s3p2d2","Nb_PBE19"],
                            "Mo" : ["Mo7.0-s3p2d2f1","Mo_PBE19"],
                            "Tc" : ["Tc7.0-s3p2d2f1","Tc_PBE19"],
                            "Ru" : ["Ru7.0-s2p2d2f1","Ru_PBE19"],
                            "Rh" : ["Rh7.0-s2p2d2f1","Rh_PBE19"],
                            "Pd" : ["Pd7.0-s2p2d2f1","Pd_PBE19"],
                            "Ag" : ["Ag7.0-s2p2d2f1","Ag_PBE19"],
                            "Cd" : ["Cd7.0-s2p1d2f1","Cd_PBE19"],
                            "In" : ["In7.0-s2p2d2f1","In_PBE19"],
                            "Sn" : ["Sn7.0-s2p2d3f1","Sn_PBE19"],
                            "Sb" : ["Sb7.0-s3p3d3f2","Sb_PBE19"],
                            "Te" : ["Te7.0-s3p3d2f1","Te_PBE19"],
                            "I"  : ["I7.0-s3p3d2f1","I_PBE19"],
                            "Xe" : ["Xe11.0-s3p2d2f1","Xe_PBE19"],
                            "Cs" : ["Cs12.0-s3p2d2f2","Cs_PBE19"],
                            "Ba" : ["Ba10.0-s3p2d2f2","Ba_PBE19"],}

class OpenMXInputWriter(object):
    def __init__(self, structure : Structure):
        self._openmx_in_text = ""
        self._structure = structure
        self._System_Name = "openmx"
        self._DATA_PATH = ""
        self._HS_fileout = "on"
        self._Atoms_SpeciesAndCoordinates_Unit = "Ang"
        self._Species_Number = 0
        self._Definition_of_Atomic_Species = ""
        self._Atoms_Number = 0
        self._Atoms_SpeciesAndCoordinates = ""
        self._scf_XcType = "GGA-PBE"
        self._scf_ElectronicTemperature = 300.0
        self._scf_energycutoff = 300
        self._scf_maxIter = 2000
        self._scf_EigenvalueSolver = "Band"
        self._scf_Kgrid = [5, 5, 1]
        self._scf_Criterion = "1.0e-6"
        self._scf_partialCoreCorrection = "on"
        self._scf_SpinPolarization = "nc"
        self._scf_SpinOrbit_Coupling = "on"
        self._scf_Mixing_Type = "RMM-DIISK"
        self._scf_Init_Mixing_Weight = 0.3
        self._scf_Mixing_History = 30
        self._scf_Mixing_StartPulay = 6
        self._scf_Mixing_EveryPulay = 1
        self._1DFFT_EnergyCutoff = 3600
        self._1DFFT_NumGridK = 900
        self._1DFFT_NumGridR = 900
        self._scf_ProExpn_VNA = "off"
        self._MD_Type = "Nomd"

        self._structure_analyze()
        pass

    def _struct(self):
        if self._DATA_PATH == "":
            print("No DFT_DATA path specified.")
            return False

        self._openmx_in_text += "System.Name                           {}\n".format(self._System_Name)
        self._openmx_in_text += "DATA.PATH                             {}\n".format(self._DATA_PATH)
        self._openmx_in_text += "HS.fileout                            {}\n".format(self._HS_fileout)
        self._openmx_in_text += "\n"
        self._openmx_in_text += "Species.Number                        {}\n".format(self._Species_Number)
        self._openmx_in_text += "<Definition.of.Atomic.Species\n"
        self._openmx_in_text += self._Definition_of_Atomic_Species
        self._openmx_in_text += "Definition.of.Atomic.Species>\n"
        self._openmx_in_text += "Atoms.Number                          {}\n".format(self._Atoms_Number)
        self._openmx_in_text += "Atoms.SpeciesAndCoordinates.Unit      {}\n".format(self._Atoms_SpeciesAndCoordinates_Unit)
        self._openmx_in_text += "<Atoms.SpeciesAndCoordinates\n"
        self._openmx_in_text += self._Atoms_SpeciesAndCoordinates
        self._openmx_in_text += "Atoms.SpeciesAndCoordinates>\n"
        self._openmx_in_text += "\n"
        self._openmx_in_text += "scf.XcType                            {}\n".format(self._scf_XcType)
        self._openmx_in_text += "scf.ElectronicTemperature             {}\n".format(self._scf_ElectronicTemperature)
        self._openmx_in_text += "scf.energycutoff                      {}\n".format(self._scf_energycutoff)
        self._openmx_in_text += "scf.maxIter                           {}\n".format(self._scf_maxIter)
        self._openmx_in_text += "scf.EigenvalueSolver                  {}\n".format(self._scf_EigenvalueSolver)
        self._openmx_in_text += "scf.Kgrid                             {} {} {}\n".format(self._scf_Kgrid[0], self._scf_Kgrid[1], self._scf_Kgrid[2])
        self._openmx_in_text += "scf.criterion                         {}\n".format(self.scf_criterion)
        self._openmx_in_text += "scf.partialCoreCorrection             {}\n".format(self._scf_partialCoreCorrection)
        self._openmx_in_text += "\n"
        self._openmx_in_text += "scf.SpinPolarization                  {}\n".format(self._scf_SpinPolarization)
        self._openmx_in_text += "scf.SpinOrbit.Coupling                {}\n".format(self._scf_SpinOrbit_Coupling)
        self._openmx_in_text += "\n"
        self._openmx_in_text += "scf.Mixing.Type                       {}\n".format(self._scf_Mixing_Type)
        self._openmx_in_text += "scf.Init.Mixing.Weight                {}\n".format(self._scf_Init_Mixing_Weight)
        self._openmx_in_text += "scf.Mixing.History                    {}\n".format(self._scf_Mixing_History)
        self._openmx_in_text += "scf.Mixing.StartPulay                 {}\n".format(self._scf_Mixing_StartPulay)
        self._openmx_in_text += "scf.Mixing.EveryPulay                 {}\n".format(self._scf_Mixing_EveryPulay)
        self._openmx_in_text += "\n"
        self._openmx_in_text += "1DFFT.EnergyCutoff                    {}\n".format(self._1DFFT_EnergyCutoff)
        self._openmx_in_text += "1DFFT.NumGridK                        {}\n".format(self._1DFFT_NumGridK)
        self._openmx_in_text += "1DFFT.NumGridR                        {}\n".format(self._1DFFT_NumGridR)
        self._openmx_in_text += "\n"
        self._openmx_in_text += "scf.ProExpn.VNA                       {}\n".format(self._scf_ProExpn_VNA)
        self._openmx_in_text += "\n"
        self._openmx_in_text += "MD.Type                               {}\n".format(self._MD_Type)
        self._openmx_in_text += "### END ###"


    def _structure_analyze(self):
        species = []
        for atom in self._structure.atom_list:
            if not atom in species:
                species.append(atom)
        self._Species_Number = len(species)
        for specie in species:
            if specie in basis_configuration_dict.keys():
                self._Definition_of_Atomic_Species +=  (
                    "  {:<4}   {:<20}   {:<15}\n".format(specie,
                                              basis_configuration_dict[specie][0],
                                              basis_configuration_dict[specie][1]))
            else:
                print("Specie '" + specie + "' not defined.")
                return False
        self._Atoms_Number = self._structure.atom_num
        for position,coordinate in enumerate(self._structure.coordinate):
            element = self._structure.atom_list[position]
            valence_electron_num = Pt.get_valence_electron_num(element)
            spin = float(valence_electron_num/2)
            self._Atoms_SpeciesAndCoordinates \
                += ("  {:<8}   {:<8}      {:.10f}    {:.10f}    {:.10f}     {:.1f}   {:.1f}\n"
                    .format(position,element,float(coordinate[0]),float(coordinate[1]),float(coordinate[2]),spin,spin))
        return True

    def write_openmx_input_file(self,path,filename = "openmx_in.dat"):
        self._struct()
        with open(path + "/" + filename, "w") as file:
            file.write(self._openmx_in_text)
            file.close()
        return

    def system_name(self,arg):
        self._System_Name = arg
        return True

    def data_path(self,arg):
        self._DATA_PATH = arg
        return True

    def hs_fileout(self,arg):
        self.HS_file = arg
        return True

    def atoms_species_and_coordinates_unit(self,arg):
        if not arg in ["Ang","Au","Frac"]:
            raise ValueError("Argument '" + arg + "' not recognized.It should Ang,Au or Frac.")
        self._Atoms_SpeciesAndCoordinates = arg
        return True

    def scf_xctype(self,arg):
        if not arg in ["LDA","LSDA-CA","LSDA-PW","GGA-PBE"]:
            raise ValueError("Argument '" + arg + "' not recognized.It,should be LDA,LSDA-CA,LSDA-PW or GGA-PBE.")
        self.XcType = arg
        return True

    def scf_electronic_temperature(self,arg):
        self._scf_ElectronicTemperature = float(arg)
        return True

    def scf_energycutoff(self,arg):
        self._scf_energycutoff = float(arg)
        return True

    def scf_maxiter(self,arg):
        self._scf_maxIter = int(arg)
        return True

    def scf_eigenvaluesolver(self,arg):
        if not arg in ["Band","DC","DC-LNO","Krylov","ON2","Cluster"]:
            raise ValueError("Argument '" + arg + "' not recognized.It should be Band,DC,DC-LNO,Krylov,ON2,Cluster")
        self._scf_EigenvalueSolver = arg
        return True

    def scf_kgrid(self,arg_list):
        self._scf_Kgrid = arg_list
        return True

    def scf_criterion(self,arg):
        self.scf_criterion = arg
        return True

    def scf_partialcorecorrection(self,arg):
        self._scf_partialCoreCorrection = arg
        return True

    def scf_spinpolarization(self,arg):
        self._scf_SpinPolarization = arg
        return True

    def scf_spinorbit_coupling(self,arg):
        self._scf_SpinOrbit_Coupling = arg
        return True

    def scf_mixing_type(self):
        self._scf_Mixing_Type = arg
        return True

    def scf_init_mixing_weight(self,arg):
        self._scf_Init_Mixing_Weight = float(arg)
        return True

    def scf_mixing_history(self,arg):
        self._scf_Mixing_History = int(arg)
        return True

    def scf_mixing_startpulay(self,arg):
        self._scf_Mixing_StartPulay = int(arg)
        return True

    def scf_mixing_everypulay(self,arg):
        self._scf_Mixing_EveryPulay = int(arg)
        return True

    def dfft_energycutoff(self,arg):
        self._1DFFT_EnergyCutoff = float(arg)
        return True

    def dfft_numgridk(self,arg):
        self._1DFFT_NumGridK = int(arg)
        return True

    def dfft_numgridr(self,arg):
        self._1DFFT_NumGridR = int(arg)
        return True

    def scf_proexpn_vna(self,arg):
        self.scf_proExpn_VNA = arg
        return True

    def md_type(self,arg):
        self._MD_Type = arg
        return True