import serial

ser = serial.Serial('COM3', 9600, timeout = 1)
ser.flush()

def driveStraight(tgt):
    message = f"DRIVE {tgt}\n"
    ser.write(message.encode())

def rotate(tgt):
    message = f"ROTATE {tgt}\n"
    ser.write(message.encode())

def stop():
    ser.write(b"STOP\n")

def start():
    ser.write(b"CONTINUE\n")