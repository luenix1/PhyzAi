import CardDetection
import Listener
import Variables
import cv2 as cv
import keyboard
import time
import pyaudio
import PlayGame

cap = cv.VideoCapture(0,cv.CAP_DSHOW)

CHANNELS = 1
FRAME_RATE = 16000
FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

OUTPUT_FILE = 'tempRecording.wav'



pressedQ = False

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = FRAME_RATE,
                input = True,
                input_device_index = 2,
                frames_per_buffer= 1024)

#initialize deck
def getCard():
    while True:
        ret, frame = cap.read()
        card, gotCard = CardDetection.detectCard(frame)
        print(card)
        if cv.waitKey(1) & gotCard:
            cap.release()
            cv.destroyAllWindows()
            Variables.currentCards.append(card)
            break

getCard()

print(Variables.currentCards)

while True:

    try:
        if keyboard.is_pressed("q"):
            if not pressedQ:
                print("recording")
            Listener.recordAudio(stream)
            pressedQ = True
            
            
            
        if not keyboard.is_pressed("q") and pressedQ:
            time.sleep(0.5)
            Listener.stopRecording(stream)
            print("done")
            Goal = Listener.searchKeyWords(OUTPUT_FILE).name
            Variables.knownCards.append(Goal)
            pressedQ = False
            response = PlayGame.haveCard(Goal, Variables.currentCards)
            print(response)
    except:
        break    







print("endLoop")
cap.release()
cv.destroyAllWindows()
