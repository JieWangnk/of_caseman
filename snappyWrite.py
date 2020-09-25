#! /usr/bin/python
import re   #regular expression operations
import math
import sys  #system-specific parameters and functions
import os   #miscellaneous operating system read/write files, manipulate paths
import xml.etree.ElementTree as ET
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile

file=ParsedParameterFile(os.path.join('system', 'snappyHexMeshDict'))

#snappyHexMesh rewrite
############################

# command-line input
help_text = """Usage: automesh.py [edge refinement] [min surface refinement] [max surface refinement] [resolve FeatureAngle] [num of addLayer]"""

try:    #try block lets you test a block of code for errors
    if len(sys.argv) > 1:
        for input in sys.argv[1:]:
            edgeRefinement = sys.argv[1]
            minSurfaceRefinement = sys.argv[2]
            maxSurfaceRefinement = sys.argv[3]
            resolveFeatureAngle = sys.argv[4]
            addLayerNum = sys.argv[5]
    else:
        edgeRefinement = 5
        minSurfaceRefinement = 2
        maxSurfaceRefinement = 4
        resolveFeatureAngle = 10
        addLayerNum = 3
        print("Apply default setting to snappyHexMesh: 5 2 4 10 3")
except:     #expect block lets you handel the error
    print (sys.argv)
    print (help_text)
    sys.exit()      #exit from python, cleanup the actions action specified by finally clauses of try statements

print ("edge Refinement level: {}".format(edgeRefinement))
print ("minimum SurfaceRefinement: {}".format(minSurfaceRefinement))
print ("maximum SurfaceRefinement: {}".format(maxSurfaceRefinement))
print ("resolve FeatureAngle: {}".format(resolveFeatureAngle))
print ("number of addLayer: {}".format(addLayerNum))

#assert file["deltaT"]=="theVertices"

for i in range(len(file["castellatedMeshControls"]["features"])):
    file["castellatedMeshControls"]["features"][i]["level"]= format(edgeRefinement)

for wall in file["castellatedMeshControls"]["refinementSurfaces"]:
    file["castellatedMeshControls"]["refinementSurfaces"][wall]["level"]= ("(" + str(minSurfaceRefinement) + " " + str(maxSurfaceRefinement) + ")")

file["castellatedMeshControls"]["resolveFeatureAngle"]= format(resolveFeatureAngle)

file["addLayersControls"]["layers"]["wall_aorta"]["nSurfaceLayers"]=format(addLayerNum)

file.writeFile()
#print(file)
print ("snappyHexMeshDict ReWrite done.")
