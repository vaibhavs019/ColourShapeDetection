import cv2 
import numpy as np

def getContours(img,color):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 700.0:
            print(area)
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(imgContour, color,
                        (x+(w//2)-10, y+(h//2)-10), cv2.FONT_HERSHEY_SCRIPT_COMPLEX , 0.7,
                        (0, 0, 0), 2)



real_colors = {
    "yellow": [48, 212, 237],
    "red": [62, 54, 220],
    #"white": [237, 232, 221],
    "green": [137, 215, 11],
    "Orange": [96,202,240]
}
val = 40

cap = cv2.VideoCapture(0)

while(True):

    ret, img = cap.read()
    if img is not None:
        imgContour = img.copy()
        for color in real_colors:
            lower = np.array(real_colors[color]) - np.array([val, val, val])
            upper = np.array(real_colors[color]) + np.array([val, val, val])
            mask = cv2.inRange(img, lower, upper)
            getContours(mask,color)
            
        cv2.imshow("All Images Stacked Window", np.hstack([img,imgContour]))
    q = cv2.waitKey(1)
    if q == ord("q"):
        break
cv2.destroyAllWindows()