import cv2
import numpy as np

im = cv2.imread("sample.bmp")
im = cv2.imread("Application2.ppm")
print(cv2.__version__)

print(im.size)

print( im.dtype )
print( im.nbytes / im.size )
ret,im2 = cv2.threshold(im,160,255,cv2.THRESH_BINARY)
print( im2.dtype )
print( im2.nbytes / im2.size )

kernel = np.ones((7,7),np.uint8)
print( kernel.dtype )
print( kernel.nbytes / kernel.size )
im3 = cv2.erode(im2, kernel);
im2 = cv2.erode(im3, kernel);
im3 = cv2.erode(im2, kernel);
im2 = cv2.erode(im3, kernel);
im3 = cv2.dilate(im2, kernel);
im2 = cv2.dilate(im3, kernel);
im3 = cv2.dilate(im2, kernel);
im2 = cv2.dilate(im3, kernel);


cv2.imshow("full_size",im)
cv2.waitKey(0)
cv2.imshow("full_size",im2)
cv2.waitKey(0)
