import tts
import PlayGame
import cv2 as cv
import TableDetection


cap = cv.VideoCapture(0,cv.CAP_DSHOW)

while cap.isOpened:
    ret, frame = cap.read()

    TableDetection.findTable(frame)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break
    

