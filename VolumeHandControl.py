import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(10,150)
cap.set(3, wCam)
cap.set(4, hCam)
cTime = 0
pTime = 0

detector = htm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
# drawBarMin = 400
# drawBarMax = 120

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 2)

        length = math.hypot(x2-x1,y2-y1)
        # print(length)

        # Hand range 30 - 150
        # Volume range -65 - 0

        vol = np.interp(length, [30,150], [minVol,maxVol])
        volBar = np.interp(length, [30,150], [400,120])
        volPer = np.interp(length, [30, 150], [0, 100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if volPer < 20:
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

        elif volPer > 20 and volPer < 80:
            cv2.circle(img, (cx, cy), 10, (0, 255, 255), cv2.FILLED)

        else:
            cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    if volPer < 20:
        cv2.rectangle(img, (47, 117), (88, 403), (0, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED)

    elif volPer > 20 and volPer < 80:
        cv2.rectangle(img, (47, 117), (88, 403), (0, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 255), cv2.FILLED)

    else:
        cv2.rectangle(img, (47, 117), (88, 403), (0, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN,
                2.5, (0, 0, 255), 3)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}', (10,40), cv2.FONT_HERSHEY_PLAIN,
                2.5, (255,0,50), 3)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

