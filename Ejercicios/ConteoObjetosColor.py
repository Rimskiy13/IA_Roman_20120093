import cv2 as cv

img = cv.imread("imagenes/salida.jpg", 1)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
ubb = (0, 80, 80)
uba = (10, 255, 255)

ubb2 = (170, 80, 80)
uba2 = (180,255,255)

mask1 = cv.inRange(hsv, ubb, uba)
mask2 = cv.inRange(hsv, ubb2, uba2)
mask = mask1 + mask2    

res = cv.bitwise_and(img, img, mask=mask)

cv.imshow("img", img)
cv.imshow("hsv", hsv)
cv.imshow("res", res)
cv.waitKey(0)
cv.destroyAllWindows