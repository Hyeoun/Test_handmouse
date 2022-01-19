import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

#################################
wCam, hCam = 640, 480

#################################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(maxHands=1)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    # 2. Get the tip of the index and middle fingers 손의 위치와 사각형의 좌표
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        # print(x1, y1, x2, y2)

    # 3. Check which fingers are up 구부려졌는지 확인 엄지만 구부리면 1, 나머지는 피면 1
        fingers = detector.fingersUp()
        print(fingers)
    # 4. Only Index Finger : Moving Mode
    # 5. Convert Coordicates
    # 6. Smoothen Values
    # 7. Move Mouse
    # 8. Both Index and middle fingers are up : Clicking Mode
    # 9. Find distance between fingers
    # 10. Click mouse if distance short

    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow('Image', img)
    cv2.waitKey(1)
