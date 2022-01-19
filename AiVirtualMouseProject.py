import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

#################################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 5  # 마우스를 부드럽게 움직이는 정도
#################################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()  # 화면 해상도 가져오기
# print(wScr, hScr)

while True:
    # 1. Find hand Landmarks
    success, img = cap.read()
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
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)
        # 4. Only Index Finger : Moving Mode
        if fingers[1]==1 and fingers[2]==0:  # 검지가 펴져있고 중지가 구부려져 있으면
            # 5. Convert Coordicates

            x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))  # x 좌표 구하기
            y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))  # y 좌표 구하기
            # 분홍색 상자 안에서만 작동
            # 6. Smoothen Values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. Move Mouse
            autopy.mouse.move(wScr-clocX, clocY)  # 마우스를 해당 좌표로 이동
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)  # 검지에 점 찍는다.
            plocX, plocY = clocX, clocY
        # 8. Both Index and middle fingers are up : Clicking Mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.findDistance(8, 12, img)
            # 엄지와 중지 사이의 거리 산출 및 점과 선 그리기
            print(length)
            # 10. Click mouse if distance short
            if length < 30:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()



    # 11. Frame Rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    # 12. Display
    cv2.imshow('Image', img)
    cv2.waitKey(1)
