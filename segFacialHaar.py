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
       b,g,r = cv.split(frame)
       eje = cv.merge([b,r,g])
       eje = frame[y:y+h, x:x+w]
       eje = frame[y:y+h, x:x+w]
       #frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
       #frame2 = frame[y:y+h, x:x+w]
       #frame3 = frame[y:y+h, x:x+w]

       frame2 = cv.resize(eje, (100, 100), interpolation=cv.INTER_AREA)
       frame3 = cv.resize(eje, (80, 80), interpolation=cv.INTER_AREA)
       

       #cv.imwrite('C:\Users\roman\Documents\Inteligencia Artificial\Ejercicios\frames'+str(i)+'.jpg', frame2)
       cv.imshow('Rostro 100', frame2)
       cv.imshow('Rostro 80', frame3)
    cv.imshow('Rostro', frame)
    i = i+1
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()