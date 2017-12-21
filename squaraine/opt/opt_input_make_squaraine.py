__author__ = "Thiago Lopes"
__email__ = "lopes.th.o@gmail.com"
__date__ = "2017-12-21 09:38:03"

import os
from shutil import copyfile
from find_xyz_from_a_log import Find_XYZ
dirMother = "".join([ "/"+x for x in os.getcwd().split("/")[0:-1] if len(x) >0])
dirOpt = dirMother+"/opt"
dirGeom = dirMother+"/pre_opt"

molecules = {
    "squaraine-H-NMe2" : 36, "squaraine-NMe2-NMe2" : 44, "squaraine-OMe-H" : 32,
    "squaraine-OMe-NMe2" : 37, "squaraine-OMe-OMe" : 36, "squaraine_H-H" : 28,
    "squaraine_OH-OH" : 30, "stilbene_H-H" : 54, "stilbene_O-OH" : 56, "stilbene_OH-OH" : 56
}

for molecule in list(molecules.keys()):
    geomFile = dirGeom+"/pre_opt_" + molecule
    nameFile = dirOpt+"/opt_"+ molecule
    geom = Find_XYZ(geomFile+".log", molecules[molecule]).gaussian_style()
    fileToWrite = open(nameFile+".com", "w")
    copyfile(geomFile+".chk", nameFile+".chk")
    fileToWrite.write('{}chk={}.chk \n{}nprocshared=4 \n{}mem=2000mb \n' .format("%", nameFile.split("/")[-1],"%", "%") )
    fileToWrite.write('#p opt=(ReadFC, gdiis) nosymm output=wfn wb97x/6-31++G**\n\nOptimization of the {}\n\n0 1\n' .format(nameFile))
    for atomCoord in geom:
        fileToWrite.write(atomCoord+"\n")
    fileToWrite.write("\n\n")