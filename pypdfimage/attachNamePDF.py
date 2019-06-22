# coding=Shift_JIS

import sys
import PythonMagick

fileName    = sys.argv[1]
fileNameOut = str(fileName)+".pdf"

img = PythonMagick.Image()
img.density("600x600")
img.read(fileName)

print( img.density().width() )
print( img.density().height() )
print( img.columns() )
print( img.rows() )

#img.quality(100)
#img.size("1000x1000")
#img.depth(8)

img.fillColor(PythonMagick.Color("blue"))
img.draw(PythonMagick.DrawableRectangle(10,10, 200, 200))
img.font("Arial")
img.font("@C:\Windows\Fonts\msgothic.ttc")
img.fontPointsize(40)
img.fillColor(PythonMagick.Color("red"))
img.boxColor(PythonMagick.Color("gray"))
img.draw(PythonMagick.DrawableText(40,40, u"定兼"))

img.write(fileNameOut)

