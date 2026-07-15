import pyaudio
import keyboard
import wave
import whisper 
import string
import Variables
import time


CHANNELS = 1
FRAME_RATE = 16000
FORMAT = pyaudio.paInt16
SAMPLE_SIZE = 2

OUTPUT_FILE = 'tempRecording.wav'
frames = []
pressedQ = False

#headphones index 2

p = pyaudio.PyAudio()

# for i in range(p.get_device_count()):
#     print(p.get_device_info_by_index(i))



stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = FRAME_RATE,
                input = True,
                input_device_index = 3,
                frames_per_buffer= 1024)
    

def recordAudio(stream):
    data = stream.read(1024)
    frames.append(data)

def stopRecording(stream):
    global frames
    saveToWAV(frames, FRAME_RATE, OUTPUT_FILE)
    frames = []
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("stopped recording")

def saveToWAV(data, sample_rate, output_file):
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))  
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(data))
        print("saved")

def searchKeyWords(file):

    model = whisper.load_model("base")
    result = model.transcribe(file, fp16 = False)

    transcription = result["text"]
    print(transcription)
    translating = str.maketrans('', '', string.punctuation)
    transcription = transcription.translate(translating)
    print(transcription)
    words = transcription.split()
    for i in words:
        check = i.upper()
        print(check)


        match check:
            case "ACE" | "ACES":
                return Variables.Templates.ACE
            case "TWO" | "TWOS":
                return Variables.Templates.TWO
            case "THREE" | "THREES":
                return Variables.Templates.THREE
            case "FOUR" | "FOURS":
                return Variables.Templates.FOUR
            case "FIVE" | "FIVES":
                return Variables.Templates.FIVE
            case "SIX" | "SIXES":
                return Variables.Templates.SIX
            case "SEVEN" | "SEVENS":
                return Variables.Templates.SEVEN
            case "EIGHT" | "EIGHTS":
                return Variables.Templates.EIGHT
            case "NINE" | "NINES":
                return Variables.Templates.NINE
            case "TEN" | "TENS":
                return Variables.Templates.TEN
            case "JACK" | "JACKS":
                return Variables.Templates.JACK
            case "QUEEN" | "QUEENS":
                return Variables.Templates.QUEEN
            case "KING" | "KINGS":
                return Variables.Templates.KING
            
            
           

# while True:
#     try:
#         if keyboard.is_pressed("q"):
#             if not pressedQ:
#                 print("recording")
#             recordAudio(stream)
#             pressedQ = True
            
            
            
#         if not keyboard.is_pressed("q") and pressedQ:
#             time.sleep(0.2)
#             stopRecording(stream)
#             print("done")
#             searchKeyWords(OUTPUT_FILE)
#             pressedQ = False
#             break
#     except:
#         break    
