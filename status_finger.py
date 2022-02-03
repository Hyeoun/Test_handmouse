import cv2
import numpy as np
import ReHandTrackingModule as htm
import time
import autopy

wCam, hCam = 1280, 720
frameR = 100  # Frame Reduction

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()  # 화면 해상도 가져오기

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # 손의 위치와 사각형의 좌표
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up 구부려졌는지 확인 피면 1 구브리면 0
        fingers = detector.fingersUp()
        # print(fingers)
        cv2.putText(img, str(fingers), (20, 430), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255),3)



    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow('Image', img)
    cv2.waitKey(1)
