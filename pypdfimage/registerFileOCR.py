# coding=Shift_JIS


import sys
import PythonMagick
from PIL import Image
import pyocr
import tkinter
import cv2
import numpy as np
import subprocess
import zenhan
import re


# File Names
fileName = sys.argv[1]
fileNamePPM = str(fileName)+".ppm"

# Read PDF
#cmd = '"C:\\Program Files\\gs\\gs9.23\\bin\\gswin64c.exe" -dSAFER -dBATCH -dNOPAUSE -sDEVICE=ppm -r600 -sOutputFile="' + fileNamePPM + '" "' + fileName + '"'
#print(cmd)
#res = subprocess.run(cmd, shell=True, check=True)
#print("GS")

img = PythonMagick.Image()
img.density("300x300") #dpi
img.read(fileName+"[0]") # read only the first page
print("read PDF")
rows = img.rows()
cols = img.columns()
print(rows)
print(cols)
#img.crop( PythonMagick.Geometry(round(img.columns()/5),round(img.rows()/7), 100,500) )
#img.depth(8)
img.write(fileNamePPM)
print("Magick")

# OpenCV (Image processing)
#print(cv2.__version__)
im = cv2.imread(fileNamePPM)
height = im.shape[0]
width = im.shape[1]
im2 = im[round(height/5):round(height/5)+round(height/16), round(width/3):round(width/3)+round(width/4)]
ret,im2 = cv2.threshold(im2,180,255,cv2.THRESH_BINARY)
cv2.imwrite(fileNamePPM, im2)
print("OpenCV")


# OCR
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
#print("Will use tool '%s'" % (tool.get_name()))
#langs = tool.get_available_languages()
#print("Available languages: %s" % ", ".join(langs))
txt = tool.image_to_string(
    Image.open(fileNamePPM),
    lang="eng",
    builder=pyocr.builders.TextBuilder(tesseract_layout=3)
)
txt=txt[0:11]
print("OCR")


# Popup Dialog
def pushed():
  value = EditBox.get()
  print(value)
  sys.exit(0)

value = zenhan.z2h(txt) # zenkaku -> hankaku
value = re.sub(r'[^a-zA-Z0-9]', '#', value) # non-ascii -> ?

root = tkinter.Tk()
root.title(u"依頼書登録")
tkinter.Label(text=u'依頼番号を入力してください', font=("",16)).pack(pady=5)
img = tkinter.PhotoImage(file = fileNamePPM)
img = img.zoom(1).subsample(1)
tkinter.Label(root, image = img, borderwidth=1, bg="black", relief="flat").pack(pady=5,padx=5)
EditBox = tkinter.Entry(width=11,font=("",16))
EditBox.insert(tkinter.END, value)
EditBox.pack(pady=5)
button = tkinter.Button(root, text="OK", command=pushed, font=("",16))
button.pack(pady=5)


root.mainloop()


