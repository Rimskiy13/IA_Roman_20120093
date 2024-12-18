import numpy as np
import cv2 as cv
import math 

rostro = cv.CascadeClassifier('xmls/haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0  
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in rostros:
       frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
       gray = frame[y:y+h, x:x+w]
       gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

       frame2 = cv.resize(gray, (100, 100), interpolation=cv.INTER_AREA)
       frame3 = cv.resize(gray, (80, 80), interpolation=cv.INTER_AREA)

       ubb = (0, 20, 130)
       uba = (25, 150, 255)

       ubb2 = (5, 50, 80)
       uba2 = (50,170,255)

       mask1 = cv.inRange(frame2, ubb, uba)
       mask2 = cv.inRange(frame2, ubb2, uba2)
       mask = mask1 + mask2

       res = cv.bitwise_and(frame2, frame2, mask=mask)

       cv.imwrite('C:/Users/roman/Documents/Inteligencia Artificial/Ejercicios/frames/Gris100/'+str(i)+'.jpg', frame2)
       cv.imwrite('C:/Users/roman/Documents/Inteligencia Artificial/Ejercicios/frames/Gris80/'+str(i)+'.jpg', frame3)
       
       cv.imwrite('C:/Users/roman/Documents/Inteligencia Artificial/Ejercicios/frames/BN100/'+str(i)+'.png', res)

       cv.imshow('Rostro 100 - Gris', frame2)
       cv.imshow('Rostro 80', frame3)
       cv.imshow('Rostro 100 - BN', res)
    cv.imshow('Rostro', frame)
    i = i+1
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()

