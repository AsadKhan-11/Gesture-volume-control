import cv2
import numpy as nump
import time
import HandTrackingModule as htm
import mediapipe as mp
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

hCam , wCam  = 480 , 640


cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0


detector = htm.handDetector(detection_con=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate( IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.GetMute()
volume.GetMasterVolumeLevel()
volRange =  volume.GetVolumeRange()
# To get the range of the volume

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 0



while True:
    success, img = cap.read()

    img = detector.find_hands(img)
    lmList= detector.find_position(img , draw=False)
    
    if len(lmList) > 8:
        try:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx , cy = (x1+x2)//2 , (y1+y2)//2
            

            cv2.circle(img,(x1,y1), 12, (255,0,0), cv2.FILLED)
            cv2.circle(img,(x2,y2), 12, (255,0,0), cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
            cv2.circle(img , (cx , cy ), 8 , (255,0,0),cv2.FILLED)

            length = math.hypot(x2-x1, y2-y1)

            
            vol = nump.interp(length,[50,250],[minVol,maxVol])
            volBar = nump.interp(length,[50,250],[400,150])
            volume.SetMasterVolumeLevel(vol, None)
            # print(vol)
            
            if length<50 :
                cv2.circle(img , (cx , cy ), 8 , (255 , 255 , 0) , cv2.FILLED)

            cv2.rectangle(img,(50,150),(85,400),(0,255,0))        
            cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)        



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
