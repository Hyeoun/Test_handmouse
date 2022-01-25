import threading
from CustomHandTrackingModule import HandDetector
import cv2
import time, math, pyautogui

pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=2)
big_word_flag = False
eng_word = [['.', ',', '?', '!'], ['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i'],
            ['j', 'k', 'l'], ['m', 'n', 'o'], ['p', 'q', 'r', 's'],
            ['t', 'u', 'v'], ['w', 'x', 'y', 'z'], ['toggle']]
input_status = True
temp_arr = []


def Input_finger(fingers, st):
    if fingers[0] == 0:
        return eng_word[0 + st]
    elif fingers[1] == 0:
        return eng_word[1 + st]
    elif fingers[2] == 0:
        return eng_word[2 + st]
    elif fingers[3] == 0 and fingers[4] == 1:
        return eng_word[3 + st]
    elif fingers[4] == 0:
        return eng_word[4 + st]
    elif fingers[2] == 0 and fingers[3] == 0:
        return 'space'

def choice_word(fingers, word_arr):
    if word_arr[0] == 'toggle': return 'toggle'
    try:
        if fingers[0] == 0: return word_arr[0]
        elif fingers[1] == 0: return word_arr[1]
        elif fingers[2] == 0: return word_arr[2]
        elif fingers[3] == 0: return word_arr[3]
    except: return ''

def judge_space_toggle(arr, fl=False):
    if fl and arr[0] == 'space':
        return True, arr[0], False
    if arr[0] == 'toggle':
        return True, '', True
    return False, '', False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    input_word = ''

    if hands:
        lmList = hands[0]['lmList']  # 점의 좌표 수신
        fingers = detector.fingersUp(hands[0])
        x1, y1, x2, y2 = lmList[0][0], lmList[0][1], lmList[9][0], lmList[9][1]
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if input_status and fingers != [1, 1, 1, 1, 1]:
            if math.sin((math.pi / 2) - (math.pi / 6)) < (abs(y2 - y1) / distance):
                temp_arr = Input_finger(fingers, 0)
                input_status = False
                input_status, input_word, big_word_flag = judge_space_toggle(temp_arr)
            elif 0 < (abs(y2 - y1) / distance) < math.sin(math.pi / 6):
                temp_arr = Input_finger(fingers, 5)
                input_status = False
                input_status, input_word, big_word_flag = judge_space_toggle(temp_arr, fl=True)

        else: input_word = choice_word(fingers, temp_arr)

        if big_word_flag:
            pyautogui.hotkey('shift', input_word)
            big_word_flag = False
        else: pyautogui.press(input_word)

    # Frame Rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)