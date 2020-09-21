#! /usr/bin/python
import re   #regular expression operations
import math
import sys  #system-specific parameters and functions
import os   #miscellaneous operating system read/write files, manipulate paths
import xml.etree.ElementTree as ET
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

#merge stl files

# the directory of your STL files
directory = "./constant/triSurface/"

# STL files that will be merged into one
input_names = [
    "inlet",
    "outlet1",
    "outlet2",
    "outlet3",
    "outlet4",
    "wall_aorta"
]
# name of the output STL file
output_name = "aorta_merged"

extension = ".stl"

output_file = open(output_name + extension, "w")
for name in input_names:
    f = open(directory + name + extension, "r")

    line = f.readline()
    output_file.write("solid " + name + "\n")

    line = f.readline()
    while line != "":
        output_file.write(line)
        line = f.readline()

    f.close()
output_file.close()
print (output_name + extension, "is done.")

os.path.join("./constant/triSurface/", output_name + extension)

#blockMesh rewrite
############################

# command-line input
help_text = """Usage: makeBMD.py <file> <hex size [m]> [expand_factor] """

try:    #try block lets you test a block of code for errors
    if len(sys.argv) < 2:   #sys.argv the list of commend arguments passed to a Python script
        raise ValueError

    file_name = output_name + extension
    cell_size = float(sys.argv[1])  #18000

    if len(sys.argv) >2:
        expand_factor = float(sys.argv[2])
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

vertex_max_geo = [-1e+12, -1e+12, -1e+12]           #vertex from original geometry
vertex_min_geo = [ 1e+12,  1e+12,  1e+12]
vertex_max_exp = [-1e+12, -1e+12, -1e+12]           #vertex from expand geometry for blockMesh geometry
vertex_min_exp = [ 1e+12,  1e+12,  1e+12]
# stroll through the file and find points with highest/lowest coordinates
with open(file_name, 'r') as f:   #open for reading
    for line in f:
        m = vertex_re.match(line)

        if m:
            n = line.split()    #split a string into a list
            v = [float(n[i]) for i in range(1, 4)]

            vertex_max_geo = [max([vertex_max_geo[i], v[i]]) for i in range(3)]
            vertex_min_geo = [min([vertex_min_geo[i], v[i]]) for i in range(3)]

# scale the blockmesh by a small factor
# scale around object center, not coordinate origin!
for i in range(3):
    center = (vertex_max_geo[i] + vertex_min_geo[i])/2
    size = vertex_max_geo[i] - vertex_min_geo[i]

    vertex_max_exp[i] = center + size/2*expand_factor
    vertex_min_exp[i] = center - size/2*expand_factor

# find out number of elements that will produce desired cell size
sizes = [vertex_max_exp[i] - vertex_min_exp[i] for i in range(3)]
num_elements = [int(math.ceil(sizes[i]/cell_size)) for i in range(3)]


print ("max: {}".format(vertex_max_exp))
print ("min: {}".format(vertex_min_exp))
print ("sizes: {}".format(sizes))
print ("number of elements: {}".format(num_elements))
print ("expand factor: {}".format(expand_factor))

# write a blockMeshDict file
file=ParsedParameterFile(os.path.join('system', 'blockMeshDict'))
#assert file["deltaT"]=="theVertices"
vertex_1=[vertex_min_exp[0], vertex_min_exp[1], vertex_min_exp[2]]
vertex_2=[vertex_max_exp[0], vertex_min_exp[1], vertex_min_exp[2]]
vertex_3=[vertex_max_exp[0], vertex_max_exp[1], vertex_min_exp[2]]
vertex_4=[vertex_min_exp[0], vertex_max_exp[1], vertex_min_exp[2]]
vertex_5=[vertex_min_exp[0], vertex_min_exp[1], vertex_max_exp[2]]
vertex_6=[vertex_max_exp[0], vertex_min_exp[1], vertex_max_exp[2]]
vertex_7=[vertex_max_exp[0], vertex_max_exp[1], vertex_max_exp[2]]
vertex_8=[vertex_min_exp[0], vertex_max_exp[1], vertex_max_exp[2]]

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

#create xml files
####################################
root = ET.Element('root')
parameterList = ET.SubElement(root, 'parameterList')
maxvertex_geo = ET.SubElement(parameterList, 'parameter0_1')
minvertex_geo = ET.SubElement(parameterList, 'parameter0_2')
maxvertex_exp = ET.SubElement(parameterList, 'parameter1_1')
minvertex_exp = ET.SubElement(parameterList, 'parameter1_2')
blocksize = ET.SubElement(parameterList,'parameter2')
blockelement =ET.SubElement(parameterList,'parameter3')
blockexpension = ET.SubElement(parameterList,'parameter4')

maxvertex_geo.set('name','maximum vertex geometry')
minvertex_geo.set('name','minimum vertex geometry')
maxvertex_exp.set('name','maximum vertex blockMesh')
minvertex_exp.set('name','minimum vertex blockMesh')
blocksize.set('name','blockMesh size')
blockelement.set('name','blockMesh element')
blockexpension.set('name', 'blockMesh expension factor')

maxvertex_geo.text = format(vertex_max_geo)
minvertex_geo.text = format(vertex_min_geo)
maxvertex_exp.text = format(vertex_max_exp)
minvertex_exp.text = format(vertex_min_exp)
blocksize.text = format(sizes)
blockelement.text = format(num_elements)
blockexpension.text = format(expand_factor)

mydata = ET.tostring(root, encoding='unicode')
with open("parameterList.xml","w") as f:
    f.write(mydata)
for child in root.iter():
    print(child.tag,child.attrib,child.text)


