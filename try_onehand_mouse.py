from CustomHandTrackingModule import HandDetector
import cv2, cvzone
import time, math, pyautogui, autopy
from threading import Thread

pTime = 0
mouse_x, mouse_y, pfx, pfy = 0, 0, 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)
right_status, left_status = True, True

def mouse_Right_click():
    global right_status
    if right_status:
        pyautogui.click(x=mouse_x, y=mouse_y, button="right")
        time.sleep(0.05)

def mouse_Left_click():
    global left_status
    if left_status:
        pyautogui.click(x=mouse_x, y=mouse_y)
        time.sleep(0.05)

def move_mouse(x, y):  # 마우스를 얼마큼 움직인다.
    pyautogui.moveRel(x, y)

def judge_finger(fx, fy, sx, sy, zx, zy): # 손 끝과 첫번째 마디 비교
    f_line = ((fx-zx)**2 + (fy-zy)**2)**0.5
    s_line = ((sx-zx)**2 + (sy-zy)**2)**0.5
    if f_line > s_line: return False
    else: return True

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # 좌우반전, -1은 상하반전
    hands, img = detector.findHands(img, flipType=False)  # 손 찾기 함수, flipType= 반전 여부 확인

    if hands:
        mouse_x, mouse_y = pyautogui.position()  # 마우스 현재 좌표
        lmList = hands[0]['lmList']  # 손의 좌표를 할당받는다.
        fingers = detector.fingersUp(hands[0])  # 각 손가락 접혔는지 확인
        z_point = [lmList[0][0], lmList[0][1]]  # 손바닥의 점좌표 할당
        left_status = judge_finger(lmList[8][0], lmList[8][1], lmList[7][0], lmList[7][1], z_point[0], z_point[1])  # 검지 좌표 두개 비교
        right_status = judge_finger(lmList[12][0], lmList[12][1], lmList[11][0], lmList[11][1], z_point[0], z_point[1])  # 중지 좌표 두개 비교

        nfx, nfy = lmList[5]  # 5번점 좌표
        if [pfx, pfy] == [0, 0]: pfx, pfy = nfx, nfy  # 최초동작시 오류방지를 위해 최초 좌표 할당
        move_x, move_y = (nfx - pfx), (nfy - pfy)  # 마우스 얼마큼 움직이는지 계산
        print(left_status, right_status)
        if fingers == [1, 1, 1, 1, 1]:
            print('drop mouse')
        elif [fingers[3], fingers[4]] == [0, 0]:  # 마우스 사용시작
            tm = Thread(target=move_mouse, args=(move_x, move_y))
            tm.start()
            t1 = Thread(target=mouse_Right_click)
            t2 = Thread(target=mouse_Left_click)
            t1.start()
            t2.start()

        pfx, pfy = nfx, nfy


    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)