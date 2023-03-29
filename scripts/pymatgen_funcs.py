from pymatgen.io.xyz import XYZ
from pymatgen.io.cif import CifParser
from pymatgen.core import Structure,Molecule
from pymatgen.analysis.local_env import NearNeighbors,OpenBabelNN,Critic2NN

Parser=CifParser("./data/881852.cif")
structure=Parser.get_structures()
xyz=XYZ(structure)
xyz.write_file("./data/881852.xyz")


xyz=XYZ.from_file("./data/881852.xyz")
cif=CifParser("./data/881852.cif")
structure=Structure.from_file("./data/881852.cif")
molecule=Molecule.from_file("./data/881852.xyz")
#finder=connectivity_finder.ConnectivityFinder()
#connectivity=finder.get_structure_connectivity(xyz.molecule)
#graph=OpenBabelNN().get_bonded_structure(molecule)
graph=NearNeighbors().get_bonded_structure(structure,on_disorder="take_majority_strict")
#graph=Critic2NN().get_bonded_structure(structure)
print(1)

