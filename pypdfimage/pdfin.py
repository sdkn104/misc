# coding=Shift_JIS

import PythonMagick
import sys

fileName = sys.argv[1]

img = PythonMagick.Image()
#img.density("762x762") #dpcm
img.density("300x300") #dpi
img.read(fileName+"[0]")

#img.size("2480x3508")
#img.resize(PythonMagick.Geometry(2480,3508))
rows = img.rows()
cols = img.columns()
print(rows)
print(cols)
#img.quality(100)
#img.depth(8)
#img.resolutionUnits()

img.write(fileName+".jpg")
img.write(fileName+".pdf")
img.write(fileName+".ppm")
