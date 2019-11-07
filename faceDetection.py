import numpy as np
import cv2
import pyautogui
import time

face_cascade = cv2.CascadeClassifier('opencv/data/haarcascades/haarcascade_frontalface_default.xml')
screenWidth, screenHeight = pyautogui.size()

webcam_width = 320
webcam_height = 240

def getfraction(position_in_capture,capture,screen):
    position_in_screen = (position_in_capture*screen)/capture
    return position_in_screen

cap = cv2.VideoCapture(0)
ret = cap.set(3,320)
ret = cap.set(4,240)
time.sleep(2)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        pos_x = (x+w)/2
        pos_y = (y+h)/2
        pos_x_screen = getfraction(pos_x, webcam_width, screenWidth)
        pos_y_screen = getfraction(pos_y, webcam_height, screenHeight)
        pyautogui.moveTo(pos_x_screen, pos_y_screen)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
