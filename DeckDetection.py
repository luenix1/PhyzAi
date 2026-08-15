import cv2 as cv
import numpy as np

MAX_HEIGHT = 300
MAX_WIDTH = 200
FRAME_WIDTH = 1280
CARD_WIDTH_IN = 2.5

cap = cv.VideoCapture(0,cv.CAP_DSHOW)

def detectDeck(frame):
    frame2 = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(frame2, (5,5), 0)
    ret, thresh = cv.threshold(blur, 60, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    contours, heiarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    height, width, _ = frame.shape
    cards = 0

    cv.imshow("frame", frame)
    cv.imshow("thresh", thresh)


    for cnt in contours:
        M = cv.moments(cnt)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            size = cv.contourArea(cnt)
            peri = cv.arcLength(cnt,True)
            approximation = cv.approxPolyDP(cnt,0.01*peri, True)
            if size > 10000 and size < 120000 and len(approximation) == 4:
                draw = cv.drawContours(frame, cnt, -1, (0,255,0), 10)
                cv.circle(frame, (cX, cY), 7, (255, 255, 255), -1)

                x,y,w,h = cv.boundingRect(cnt)

                inchesToPx = CARD_WIDTH_IN / w

                distToCenter = ((FRAME_WIDTH / 2) - cX) * inchesToPx

                print(distToCenter)


while True:

    ret, frame = cap.read()

    detectDeck(frame)

    if cv.waitKey(0) & 0xFF == ord("q"):
        break


print(cap.isOpened())
print("end")
cap.release()
cv.destroyAllWindows()