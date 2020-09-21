#! /usr/bin/python
import shutil
import os
# -*- coding: utf-8 -*-

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

############################
############################
############################
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

#source = "/home/jie/openFoam/aorta_liam_py/aorta_int.stl"
source =  os.path.join("./", output_name + extension)
destination = "./constant/triSurface/"

shutil.move(source, destination)