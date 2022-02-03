from CustomHandTrackingModule import HandDetector
import cv2, cvzone
import time, math, pyautogui, autopy
from threading import Thread

pTime = 0
mouse_x, mouse_y, pfx, pfy = 0, 0, 0, 0 #pfx = previous finger X, pfy = previous finger Y
move_x, move_y = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)  # 손 감지 정확도 0.8, 손 최대 개수 1개만
right_status, left_status = True, True
drag_flag, toggle_drag, t1_flag = False, True, True

def mouse_click():  # 클릭 함수
    global t1_flag
    if right_status:
        pyautogui.click(x=mouse_x, y=mouse_y, button="right")  # 버튼 디폴트는 left다.
    if left_status:
        pyautogui.click(x=mouse_x, y=mouse_y)
    time.sleep(0.05)
    t1_flag = True

def move_mouse(x, y):  # 마우스를 얼마큼 움직인다.
    pyautogui.moveRel(x, y)

def judge_finger(fx, fy, sx, sy, zx, zy):
    f_line = ((fx-zx)**2 + (fy-zy)**2)**0.5  # 펴진 손가락 끝과 손목부분 점 간 길이, first_line
    s_line = ((sx-zx)**2 + (sy-zy)**2)**0.5  # 펴진 손가락 첫번째 마디와 손목부분 점 간 길이, second_line
    if f_line > s_line: return False
    else: return True

def move_scroll():
    if move_y <= -10: # 이동된 y 좌표가 -10 이하일때
        pyautogui.scroll(-80)  # 스크롤 다운
    elif move_y >= 10:  # 이동된 y좌표가 10 이상일때
        pyautogui.scroll(80)  # 스크롤 업

def mouse_drag():
    global toggle_drag
    if drag_flag and toggle_drag:
        pyautogui.mouseDown()
        toggle_drag = False
    elif not drag_flag and not toggle_drag:
        pyautogui.mouseUp()
        toggle_drag = True

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # 좌우반전, -1은 상하반전
    hands, img = detector.findHands(img, flipType=False)  # 손 찾기 함수, flipType= 반전 여부 확인

    if hands:  # 손 감지되었을때 시작
        mouse_x, mouse_y = pyautogui.position()  # 마우스 현재 좌표
        lmList = hands[0]['lmList']  # 손의 좌표들을 할당받는다.
        fingers = detector.fingersUp(hands[0])  # 각 손가락 접혔는지 확인
        z_point = [lmList[0][0], lmList[0][1]]  # 손목부분의 점좌표 할당
        left_status = judge_finger(lmList[8][0], lmList[8][1], lmList[7][0], lmList[7][1], z_point[0], z_point[1])  # 검지상태 판단, 좌클릭
        right_status = judge_finger(lmList[12][0], lmList[12][1], lmList[11][0], lmList[11][1], z_point[0], z_point[1])  # 중지상태 판단, 우클릭

        nfx, nfy = lmList[5]  # 5번점 좌표(검지 가장 안쪽 마디), 마우스 좌표 기준이 될 것임
        if [pfx, pfy] == [0, 0]: pfx, pfy = nfx, nfy  # 최초동작시 오류방지를 위해 최초 좌표 할당
        move_x, move_y = (nfx - pfx), (nfy - pfy)  # 마우스 얼마큼 움직이는지 계산
        print(move_x, move_y)
        if fingers == [1, 1, 1, 1, 1]:  # 손가락을 모두 폈을때 마우스 동작 x
            drag_flag = False
            t3 = Thread(target=mouse_drag)
            t3.start()
        elif fingers == [1, 0, 0, 0, 1]:
            tm = Thread(target=move_mouse, args=(move_x, move_y))  # 해당 함수의 스레드 할당
            tm.start()  # 스레드 시작
            drag_flag = True
            t3 = Thread(target=mouse_drag)
            t3.start()
        elif [fingers[3], fingers[4]] == [0, 0]:  # 마우스 사용시작
            tm = Thread(target=move_mouse, args=(move_x, move_y))  # 해당 함수의 스레드 할당
            tm.start()  # 스레드 시작
            drag_flag = False
            if t1_flag:
                t1 = Thread(target=mouse_click)
                t1.start()
                t1_flag = False
            if fingers[0] == 0:
                t2 = Thread(target=move_scroll)
                t2.start()

        pfx, pfy = nfx, nfy  # 전 좌표에 현재좌표 지정


    # Frame Rate
    cTime = time.time()  # current time
    fps = 1 / (cTime - pTime)
    pTime = cTime  # previous time
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)