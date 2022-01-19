import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)


while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=True)  # with Draw  flipType = 좌우 반전
    # hands = detector.findHands(img, draw=False, flipType=False)  # No Draw
    # print(len(hands))  # hands = 손 개수

    # Hand - dict(lmList - bbox - center - type)
    if hands:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1['lmList']  # List of 21 Landmarks points
        bbox1 = hand1['bbox']  # Bounding Box info x, y, w, h
        centerPoint1 = hand1['center']  # center of the hand cx, cy
        handType1 = hand1['type']  # hand Type Left or Right

        # print(len(lmList1), lmList1)
        # print(bbox1)
        # print(centerPoint1)
        fingers1 = detector.fingersUp(hand1)

        if len(hands)==2:
            hand2 = hands[1]
            lmList2 = hand2['lmList']  # List of 21 Landmarks points
            bbox2 = hand2['bbox']  # Bounding Box info x, y, w, h
            centerPoint2 = hand2['center']  # center of the hand cx, cy
            handType2 = hand2['type']  # hand Type Left or Right

            fingers2 = detector.fingersUp(hand2)
            print(fingers1, fingers2)

    cv2.imshow('Image', img)
    cv2.waitKey(1)