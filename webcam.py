import numpy as np
import cv2

cap = cv2.VideoCapture(0)
print(cap)
ret = cap.set(3,320)
ret = cap.set(4,240)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    cv2.rectangle(frame,(384,0),(510,128),(0,255,0),10) #start x,y; end xy, rgb, line weight

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
