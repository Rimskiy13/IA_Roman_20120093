import cv2 as cv
import numpy as nump
img = cv.imread("imagenes/img1.jpg",1)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
rgb = cv.cvtColor(img, cv.COLOR_RGB2BGR)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
#x,y=img.shape
#img2 = nump.zeros((x*2,y*2), dtype='uint8')

#for i in range(x):
#    for j in range(y):
#        if(img[i, j]>150):
#            img[i, j] = 255
#        else:
#            img[i, j] = 0

#print(img.shape)
cv.imwrite('C:/Users/roman/Documents/Inteligencia Artificial/Ejercicios/imagenes/img1.jpg', gray)
cv.imshow('img',img)
cv.imshow('gray',gray)
cv.imshow('rgb',rgb)
cv.imshow('hsv',hsv)
#cv.imshow('img2',img2)
cv.waitKey(0)
cv.destroyAllWindows
