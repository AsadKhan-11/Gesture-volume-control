import cv2
import numpy as num
import time

cap = cv2.VideoCapture(0)  

while True:
    success, img = cap.read(1)
    if success:
        cv2.imshow("Img", img)
        cv2.waitKey(1)
    else:
        print("Error reading camera frame")
        break
