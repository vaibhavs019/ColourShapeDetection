import cv2
from cvzone.SerialModule import SerialObject
import numpy as np


arduino = SerialObject()

colors = {
    'red': ([0, 50, 50], [10, 255, 255]),
    'green': ([40, 50, 50], [70, 255, 255]),
    'blue': ([100, 50, 50], [140, 255, 255]),
    'yellow': ([20, 50, 50], [40, 255, 255]),
    'white': ([0, 0, 180], [180, 30, 255])
}

det = cv2.VideoCapture(0)


while True:
    ret, frame = det.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    masks = {}
    areas = {}

    for color, (lower, upper) in colors.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        masks[color] = mask

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            area = max([cv2.contourArea(c) for c in contours])
        else:
            area = 0
        areas[color] = area

    max_color = max(areas, key=areas.get)
    print(max_color)
    
    cv2.putText(frame, max_color, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if (max_color == "red"):
        arduino.sendData([0])
    elif (max_color == "green"):
        arduino.sendData([1])
    elif (max_color == "blue"):
        arduino.sendData([2])
    elif (max_color == "yellow"):
        arduino.sendData([3])
    elif (max_color == "white"):
        arduino.sendData([4])   

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

det.release()
cv2.destroyAllWindows()
