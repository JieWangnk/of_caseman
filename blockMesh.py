#! /usr/bin/python
import re   #regular expression operations
import math
import sys  #system-specific parameters and functions
import os   #miscellaneous operating system read/write files, manipulate paths
from os import path
from PyFoam.Execution.ConvergenceRunner import ConvergenceRunner
from PyFoam.Execution.UtilityRunner import UtilityRunner
from PyFoam.LogAnalysis.BoundingLogAnalyzer import BoundingLogAnalyzer
from PyFoam.RunDictionary.SolutionFile import SolutionFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


# command-line input
help_text = """Usage: makeBMD.py <file> <hex size [m]> [expand_factor] """

try:    #try block lets you test a block of code for errors
    if len(sys.argv) < 3:   #sys.argv the list of commend arguments passed to a Python script
        raise ValueError

    file_name = sys.argv[1]
    cell_size = float(sys.argv[2])  #18000

    if len(sys.argv) > 3:
        expand_factor = float(sys.argv[3])
    else:
        expand_factor = 1.001
except:     #expect block lets you handel the error
    print (sys.argv)
    print (help_text)
    sys.exit()      #exit from python, cleanup the actions action specified by finally clauses of try statements

# format of vertex files:       #stl-standard triangle language
#    vertex  7.758358e-03  2.144992e-02  1.539336e-02
#    vertex  7.761989e-03  2.167315e-02  1.525611e-02
#    vertex  7.767175e-03  2.167225e-02  1.551236e-02

# a regular expression to match a beginning of a vertex line in STL file
#re.compile(pattern,flags=0) compile a regular expression pattern into a regular expression object
#which can be used for matching using its match(),search()
vertex_re = re.compile('\s+vertex.+')   #for unicode(str)patterns

vertex_max = [-1e+12, -1e+12, -1e+12]
vertex_min = [ 1e+12,  1e+12,  1e+12]

# stroll through the file and find points with highest/lowest coordinates
with open(sys.argv[1], 'r') as f:   #open for reading
    for line in f:
        m = vertex_re.match(line)

        if m:
            n = line.split()    #split a string into a list
            v = [float(n[i]) for i in range(1, 4)]

            vertex_max = [max([vertex_max[i], v[i]]) for i in range(3)]
            vertex_min = [min([vertex_min[i], v[i]]) for i in range(3)]

# scale the blockmesh by a small factor
# achtung, scale around object center, not coordinate origin!
for i in range(3):
    center = (vertex_max[i] + vertex_min[i])/2
    size = vertex_max[i] - vertex_min[i]

    vertex_max[i] = center + size/2*expand_factor
    vertex_min[i] = center - size/2*expand_factor

# find out number of elements that will produce desired cell size
sizes = [vertex_max[i] - vertex_min[i] for i in range(3)]
num_elements = [int(math.ceil(sizes[i]/cell_size)) for i in range(3)]


print ("max: {}".format(vertex_max))
print ("min: {}".format(vertex_min))
print ("sizes: {}".format(sizes))
print ("number of elements: {}".format(num_elements))
print ("expand factor: {}".format(expand_factor))

# write a blockMeshDict file
file=ParsedParameterFile(path.join('system', 'blockMeshDict'))
#assert file["deltaT"]=="theVertices"
vertex_1=[vertex_min[0], vertex_min[1], vertex_min[2]]
vertex_2=[vertex_max[0], vertex_min[1], vertex_min[2]]
vertex_3=[vertex_max[0], vertex_max[1], vertex_min[2]]
vertex_4=[vertex_min[0], vertex_max[1], vertex_min[2]]
vertex_5=[vertex_min[0], vertex_min[1], vertex_max[2]]
vertex_6=[vertex_max[0], vertex_min[1], vertex_max[2]]
vertex_7=[vertex_max[0], vertex_max[1], vertex_max[2]]
vertex_8=[vertex_min[0], vertex_max[1], vertex_max[2]]

file["vertices"][0]=("("+ (' ').join([str(i) for i in vertex_1]) +")")
file["vertices"][1]=("("+ (' ').join([str(i) for i in vertex_2]) +")")
file["vertices"][2]=("("+ (' ').join([str(i) for i in vertex_3]) +")")
file["vertices"][3]=("("+ (' ').join([str(i) for i in vertex_4]) +")")
file["vertices"][4]=("("+ (' ').join([str(i) for i in vertex_5]) +")")
file["vertices"][5]=("("+ (' ').join([str(i) for i in vertex_6]) +")")
file["vertices"][6]=("("+ (' ').join([str(i) for i in vertex_7]) +")")
file["vertices"][7]=("("+ (' ').join([str(i) for i in vertex_8]) +")")
file["blocks"][2]=(num_elements)
file.writeFile()
#print(file)
print ("blockMesh done.")