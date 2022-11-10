import threading
import time
import cv2
import RPi.GPIO as GPIO
import numpy as np
import tensorflow as tf
import move
from tensorflow.keras.models import load_model

PWMA = 18
AIN1 = 22
AIN2 = 27

PWMB = 23
BIN1 = 25
BIN2 = 24


def motor_back(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1


def motor_go(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


def motor_stop():
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


def motor_right(speed):
    L_Motor.ChangeDutyCycle(speed)
    GPIO.output(AIN2, True)  # AIN2
    GPIO.output(AIN1, False)  # AIN1
    R_Motor.ChangeDutyCycle(0)
    GPIO.output(BIN2, False)  # BIN2
    GPIO.output(BIN1, True)  # BIN1


def motor_left(speed):
    L_Motor.ChangeDutyCycle(0)
    GPIO.output(AIN2, False)  # AIN2
    GPIO.output(AIN1, True)  # AIN1
    R_Motor.ChangeDutyCycle(speed)
    GPIO.output(BIN2, True)  # BIN2
    GPIO.output(BIN1, False)  # BIN1


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 100)
L_Motor.start(0)

R_Motor = GPIO.PWM(PWMB, 100)
R_Motor.start(0)

speedSet = 40


def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height / 2):, :, :]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    image = cv2.GaussianBlur(image, (5, 5), 0)
    _, image = cv2.threshold(image, 160, 255, cv2.THRESH_BINARY_INV)
    image = image / 255
    return image


camera = cv2.VideoCapture(-1)
camera.set(3, 640)
camera.set(4, 480)


# def main():
#     model_path = '/home/pi/AI_CAR/model/lane_navigation_final.h5'
#     model = load_model(model_path)
##model 설정
#     carState = "stop"
#
#     try:
#         while True:
#             keyValue = cv2.waitKey(1) #키보드 입력대기
#
#
#             _, image = camera.read()
#             image = cv2.flip(image, -1)
#             preprocessed = img_preprocess(image)
#             cv2.imshow('pre', preprocessed)
#
#             X = np.asarray([preprocessed])
#             whatspare = int(model.predict(X)[0])
#             print("spare is:", whatspare)
#
#             if whatspare == "nozzle":
#                 print("nozzle") # GUI로 보내기
#             elif whatspare == "pump":
#             else :
#                   print("unknown")
#
#     except KeyboardInterrupt:
#         pass

# 여기서 부터는 Tracking line

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right,GPIO.IN)
    GPIO.setup(line_pin_middle,GPIO.IN)
    GPIO.setup(line_pin_left,GPIO.IN)
    #motor.setup()

def run():
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    #print('R%d   M%d   L%d'%(status_right,status_middle,status_left))
    if status_middle == 1:
        move.move(100, 'forward', 'no', 1)
    elif status_left == 1:
        move.move(100, 'forward', 'right', 0.6)
    elif status_right == 1:
        move.move(100, 'forward', 'left', 0.6)
    else:
        move.move(100, 'backward', 'no', 1)
# 여기까지 Tracking line

if __name__ == '__main__':
    try:
        setup()
        move.setup()
        while 1:
            run()
        pass
    except KeyboardInterrupt:
        move.destroy()

    # cv2.destroyAllWindows()
