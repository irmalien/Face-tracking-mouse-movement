# TODO: Add pipenv package manager
import numpy as np
import cv2
import pyautogui
import keyboard
from helpers import getfraction, find_average, map

FACE_CASCADE = cv2.CascadeClassifier(
    './data/haarcascade_frontalface_default.xml')
MOUSE_SMOOTHNESS = 5
KEYBOARD_PRECISION = 10
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
CAPTURE = cv2.VideoCapture(0)
size = CAPTURE.set(3, CAPTURE_WIDTH)
size = CAPTURE.set(4, CAPTURE_HEIGHT)
move_mouse = False
move_keys = False
show_capture = True
movement_history = []


def position_on_screen(selected_face):
    pos_x_screen = getfraction(selected_face[5], CAPTURE_WIDTH, SCREEN_WIDTH)
    pos_y_screen = getfraction(selected_face[6], CAPTURE_HEIGHT, SCREEN_HEIGHT)
    smooth_movement(pos_x_screen, pos_y_screen, MOUSE_SMOOTHNESS)
    pos = find_average(movement_history)
    if move_mouse:
        pyautogui.moveTo(pos[0], pos[1])
    if move_keys:
        move_with_keyboard(pos[0], pos[1], SCREEN_WIDTH, SCREEN_HEIGHT)


def smooth_movement(x, y, lenght=5):
    movement_history.append([x, y])
    if len(movement_history) > lenght:
        movement_history.pop(0)
    return


def move_with_keyboard(x, y, width, height):
    number_of_keypress = KEYBOARD_PRECISION
    x = x - (width / 2)
    y = y - (height / 2)
    area_x = 'left' if x < 0 else 'right'
    area_y = 'up' if y < 0 else 'down'

    if area_x == 'left':
        steps_x = map(x, -(width / 2), 0, number_of_keypress, 0)
    else:
        steps_x = map(x, 0, width / 2, 0, number_of_keypress)

    steps_x = int(round(steps_x))
    for times in range(steps_x):
        pyautogui.press(area_x)

    if area_y == 'up':
        steps_y = map(y, -(height / 2), 0, number_of_keypress, 0)
    else:
        steps_y = map(y, 0, height / 2, 0, number_of_keypress)

    steps_y = int(round(steps_y * 2))
    for times in range(steps_y):
        pyautogui.press(area_y)


# TODO: Match loop speed to fps refresh rate with Pyglet
# TODO: Add window preview of object position on screen
while(True):
    # Set key listeners
    if keyboard.is_pressed('m'):
        move_mouse = False if move_mouse else True
        print('move mouse', move_mouse)
    if keyboard.is_pressed('k'):
        move_keys = False if move_keys else True
        print('move keyboard', move_keys)
    if keyboard.is_pressed('c'):
        show_capture = False if move_keys else True
        print('show_capture', show_capture)
    if keyboard.is_pressed('q'):
        print('Attempt to exit')
        break

    # Capture frame-by-frame
    size, frame = CAPTURE.read()
    frame = cv2.flip(frame, 1)

    # Operations on each frame
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except cv2.error as e:
        print('oopsie camera not found', e)
        CAPTURE.release()
        cv2.destroyAllWindows()
        exit()

    try:
        faces = FACE_CASCADE.detectMultiScale(gray, 1.3, 5)
    except cv2.error as e:
        print('oopsie faces not found', e)
        CAPTURE.release()
        cv2.destroyAllWindows()
        exit()

    # Recognize face and select best candidate
    selected_face = []
    for (x, y, w, h) in faces:
        candidate_face_area = w * h
        if not selected_face or candidate_face_area > selected_face[0]:
            center_x = x + (w / 2)
            center_y = y + (h / 2)
            selected_face = [candidate_face_area,
                             x, y, w, h, center_x, center_y]

    if selected_face:
        position_on_screen(selected_face)

    if show_capture:
        cv2.imshow('frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# When everything done, release the capture
print('Gracefully exiting')
CAPTURE.release()
cv2.destroyAllWindows()
