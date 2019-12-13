# TODO: Add pipenv package manager
import numpy as np
import cv2
import pyautogui
import keyboard
from position import Position
from interaction import Interaction
from draw import Draw
from framerate import Framerate

print('program started')
pyautogui.PAUSE = 0.001
FACE_CASCADE = cv2.CascadeClassifier(
    './data/haarcascade_frontalface_default.xml')
SMOOTH_POSITION = 16
KEYBOARD_PRECISION = 8
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
#SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
CAPTURE_WIDTH = 640
CAPTURE_HEIGHT = 480
CAPTURE_CROP_FACTOR = 0.7
CAPTURE = cv2.VideoCapture(0)

size = CAPTURE.set(3, CAPTURE_WIDTH)
size = CAPTURE.set(4, CAPTURE_HEIGHT)
font = cv2.FONT_HERSHEY_SIMPLEX

move_mouse = False
move_keys = False
show_capture = True

position = Position(SMOOTH_POSITION,
                    CAPTURE_WIDTH,
                    CAPTURE_HEIGHT,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    CAPTURE_CROP_FACTOR)

interaction = Interaction(KEYBOARD_PRECISION,
                          SCREEN_WIDTH,
                          SCREEN_HEIGHT)

draw = Draw()

fps = Framerate()


def position_on_screen(selected_face):
    pos = position.smooth_resized_position(selected_face[5],
                                           selected_face[6])
    if move_mouse:
        interaction.move_mouse(pos[0], pos[1])
    if move_keys:
        interaction.move_keyboard(pos[0], pos[1])

    # TODO: Match loop speed to fps refresh rate with Pyglet
    # TODO: Add window preview of object position on screen
while(True):
    fps.counter()           # 1 frame per second
    # Set key listeners
    # TODO: Find a better solution, or perhaps use cv solution if possible
    if keyboard.is_pressed('m'):
        move_mouse = False if move_mouse else True
        print('move mouse', move_mouse)
    if keyboard.is_pressed('k'):
        move_keys = False if move_keys else True
        print('move keyboard', move_keys)
    if keyboard.is_pressed('c'):
        show_capture = False if move_keys else True
        print('show_capture', show_capture)
    if keyboard.is_pressed('z'):
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
        if selected_face:
            draw.selected_face_area(gray, selected_face)
            draw.cursor_location(gray, position.crop_screen['pos'])
        draw.capture_crop_area(gray, position.crop_screen)
        draw.fps_counter(gray, fps.actual_fps)
        cv2.imshow('frame', gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
print('Gracefully exiting')
CAPTURE.release()
cv2.destroyAllWindows()
