from threading import Thread, currentThread
from CustomHandTrackingModule import HandDetector
import cv2
import time, math, pyautogui

pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=2)
eng_word = [['.', ',', '?', '!'], ['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
            ['j', 'k', 'l'], ['m', 'n', 'o'], ['p', 'q', 'r', 's'],
            ['t', 'u', 'v'], ['w', 'x', 'y', 'z'], 'toggle']
input_status, thread_flag, big_word_flag = True, True, False
temp_arr = []
input_word = ''

def Input_finger(fingers, st):
    global temp_arr, input_status, thread_flag
    if fingers[0] == 0: temp_arr = eng_word[0 + st]
    elif fingers[1] == 0: temp_arr = eng_word[1 + st]
    elif fingers[2] == 0: temp_arr = eng_word[2 + st]
    elif fingers[4] == 0: temp_arr = eng_word[4 + st]
    elif fingers[3] == 0 and fingers[4] == 1: temp_arr = eng_word[3 + st]
    elif fingers[2] == 0 and fingers[3] == 0: temp_arr = ['space']
    time.sleep(0.2)
    input_status = False
    thread_flag = True

def choice_word(fingers, word_arr):
    global input_word, thread_flag, temp_arr, input_status
    try:
        if word_arr[0] == 'space': input_word = 'space'
        if fingers[0] == 0: input_word = word_arr[0]
        elif fingers[1] == 0: input_word = word_arr[1]
        elif fingers[2] == 0: input_word = word_arr[2]
        elif fingers[3] == 0: input_word = word_arr[3]
        input_status = True
    except: input_word = ''
    time.sleep(0.2)
    thread_flag = True
    temp_arr = []

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']  # 점의 좌표 수신
        fingers = detector.fingersUp(hands[0])
        x1, y1, x2, y2 = lmList[0][0], lmList[0][1], lmList[9][0], lmList[9][1]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if fingers != [1, 1, 1, 1, 1]:
            print(temp_arr)
            print(input_word)
            if thread_flag:
                if input_status:
                    if math.sin((math.pi / 2) - (math.pi / 6)) < (abs(y2 - y1) / distance):
                        t1 = Thread(target=Input_finger, args=(fingers, 0))
                        thread_flag = False
                        t1.start()
                    elif 0 < (abs(y2 - y1) / distance) < math.sin(math.pi / 6):
                        t1 = Thread(target=Input_finger, args=(fingers, 5))
                        thread_flag = False
                        t1.start()
                else:
                    t1 = Thread(target=choice_word, args=(fingers, temp_arr))
                    thread_flag = False
                    t1.start()
        if temp_arr == 'toggle':
            big_word_flag = True
            temp_arr = []
        if input_word != '':
            if big_word_flag and input_word != 'space':
                pyautogui.hotkey('shift', input_word)
            else: pyautogui.press(input_word)
            input_word = ''




    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)