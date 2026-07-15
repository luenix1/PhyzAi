import cv2 as cv
import numpy as np


def findTable(frame):
    # BW = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(frame,(3,3),0)
    edges = cv.Canny(blur, 200, 75)
    contours, heiarchy = cv.findContours(edges, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)

    for cnt in contours:
        size = cv.contourArea(cnt)
        if size > 0:
            draw = cv.drawContours(frame, cnt, -1, (0,255,0), 10)

    cv.imshow("blur", blur)
    cv.imshow("frame", frame)
    # cv.imshow("BW", BW)
    cv.imshow("edges",edges)