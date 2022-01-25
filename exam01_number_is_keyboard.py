from pynput.keyboard import Controller
import keyboard
import time
import pyautogui
import ctypes
from ctypes import wintypes

hllDll = ctypes.ULONG_PTR = wintypes.WPARAM
VK_HANGUEL = 0x15
history_temp = []
keycode = {1:'ㅣ', 2:['·', '··'], 3:'ㅡ', 4:['ㄱ', 'ㅋ', 'ㄲ'],
           5:['ㄴ', 'ㄹ'], 6:['ㄷ', 'ㅌ', 'ㄸ'], 7:['ㅂ', 'ㅍ', 'ㅃ'],
           8:['ㅅ', 'ㅎ', 'ㅆ'], 9:['ㅈ', 'ㅊ', 'ㅉ'], 0:['ㅇ', 'ㅁ']}
Keyboard = Controller()
read_k = '-1'
print(pyautogui.KEYBOARD_KEYS)

while True:
    if keyboard.is_pressed('1'):
        pyautogui.hotkey('alt', 'tab')
        pyautogui.press('hangul')
        pyautogui.hotkey('shift', 'r')
        pyautogui.press('b')
    print('standby')
    time.sleep(0.1)
