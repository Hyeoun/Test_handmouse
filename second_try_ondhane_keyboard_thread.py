from threading import Thread, currentThread
from CustomHandTrackingModule import HandDetector
import cv2
import time, math, pyautogui

pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)
eng_word = [['.', ',', '?', '!'], ['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
            ['j', 'k', 'l'], ['m', 'n', 'o'], ['p', 'q', 'r', 's'],
            ['t', 'u', 'v'], ['w', 'x', 'y', 'z'], ['']]
input_status, thread_flag  = True, True
temp_arr, past_fingers = [''], []
input_word = ''

def Input_finger(fingers, st):
    global temp_arr, input_status, thread_flag, input_word
    if fingers == [0, 1, 1, 1, 1]:
        temp_arr = eng_word[0 + st]
        input_status = False
    elif fingers == [1, 0, 1, 1, 1]:
        temp_arr = eng_word[1 + st]
        input_status = False
    elif fingers == [1, 1, 0, 1, 1]:
        temp_arr = eng_word[2 + st]
        input_status = False
    elif fingers == [1, 1, 1, 0, 1]:
        temp_arr = eng_word[3 + st]
        input_status = False
    elif fingers == [1, 1, 1, 1, 0] or fingers == [1, 1, 1, 0, 0]:
        temp_arr = eng_word[4 + st]
        input_status = False
    elif fingers == [1, 1, 0, 0, 1]:
        temp_arr = ['']
        input_word = 'space'
        input_status = False
    time.sleep(0.2)
    thread_flag = True

def choice_word(fingers, word_arr):
    global input_word, thread_flag, temp_arr, input_status
    try:
        if word_arr[0] == 'space': input_word = 'space'
        if fingers[0] == 0: input_word = word_arr[0]
        elif fingers[1] == 0: input_word = word_arr[1]
        elif fingers[2] == 0: input_word = word_arr[2]
        elif fingers[3] == 0: input_word = word_arr[3]
    except: input_word = ''
    time.sleep(0.2)
    input_status = True
    thread_flag = True
    temp_arr = ['']

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']  # 점의 좌표 수신
        fingers = detector.fingersUp(hands[0])
        x1, y1, x2, y2 = lmList[0][0], lmList[0][1], lmList[9][0], lmList[9][1]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if fingers != [1, 1, 1, 1, 1] and past_fingers != fingers:  # 손가락이 모두 펴져 있거나 과거에 한번 동작한 것은 동작하지 않도록 한다.
            print(fingers)
            past_fingers = fingers
            if thread_flag:
                print('thread on')
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
            print('word array : {}'.format(temp_arr))
            print('chose word : {}'.format(input_word))
        elif past_fingers != fingers and fingers == [1, 1, 1, 1, 1]: past_fingers = fingers

        # if temp_arr[0] == 'toggle':  # 토글이 된다면 시프트를 누르는 플레그를 참값으로 만든다.
        #     print('use toggle')
        #     big_word_flag = True
        #     input_status = True
        #     temp_arr = ['']
        # if input_word != '':
        #     if big_word_flag and input_word != 'space':
        #         pyautogui.hotkey('shift', input_word)
        #         big_word_flag = False
        #     else: pyautogui.press(input_word)
        #     input_word = ''
        if input_word != '':
            if input_word == 'space': input_status = True
            pyautogui.press(input_word)
            input_word = ''



    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)