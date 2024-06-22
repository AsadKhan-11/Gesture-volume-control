import cv2
import numpy as num
import time
import HandTrackingModule as htm
import mediapipe as mp


hCam , wCam  = 480 , 640



cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0


detector = htm.handDetector(detection_con=0.7)



while True:
    success, img = cap.read()

    img = detector.find_hands(img)
    lmList= detector.find_position(img , draw=False)
    
    if len(lmList) > 8:
        try:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            print("Thumb Tip:", (x1, y1))  
            print("Index Finger Tip:", (x2, y2))  

            cv2.circle(img,(x1,y1), 12, (255,0,0), cv2.FILLED)
            cv2.circle(img,(x2,y2), 12, (255,0,0), cv2.FILLED)
        except IndexError as e:
            print("IndexError occurred:", e)
    # else:
    #    print("Not enough landmarks detected")  

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
