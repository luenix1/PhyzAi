import tts
import PlayGame
import cv2 as cv
import TableDetection
import Commands
import serial
import time

# ser = serial.Serial('COM3', 9600, timeout = 1)
# ser.flush()

# cap = cv.VideoCapture(0,cv.CAP_DSHOW)

# while cap.isOpened:
#     ret, frame = cap.read()

#     TableDetection.findTable(frame)

#     if cv.waitKey(1) & 0xFF == ord("q"):
#         break

a = 0

while True:
    print(Commands.ser.readline().decode().strip())
    
    

