import cv2
import numpy as num
import time


hCam , wCam  = 480 , 640
 


cap = cv2.VideoCapture(0)  
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0

while True:
    success, img = cap.read()
    if success:

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime =  cTime


        cv2.putText(img,f'FPS:{int(fps)}',(20,40),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)


        cv2.imshow("Img", img)
        cv2.waitKey(1)


    else:
        print("Error reading camera frame")
        break
