#! /usr/bin/python
import os,sys,subprocess
import blockWrite, snappyWrite

#os.system("./blockWrite.py")
#os.system("./snappyWrite.py")

block = subprocess.run("./blockWrite.py", shell=True)
if block.stderr:
    print(f'[stderr]\n{block.stderr.decode()}')
else:
    snappy = subprocess.run("./snappyWrite.py 1 1 2 50 1", shell=True)
    if snappy.stderr:
        print(f'[stderr]\n{snappy.stderr.decode()}')
    else:
        print("New MeshDict updated")
        subprocess.run("foamCleanPolyMesh")
        subprocess.run("surfaceFeaturesDict")
        blockMesh = subprocess.run("blockMesh", shell=True)
        if blockMesh.stderr:
            print(f'[stderr]\n{blockMesh.stderr.decode()}')
        else:
            snappyMesh = subprocess.run("snappyHexMesh -overwrite", shell=True)
            if snappyMesh.stderr:
                 print(f'[stderr]\n{snappyMesh.stderr.decode()}')
            else:
                 print("Mesh finished")