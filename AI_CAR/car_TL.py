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
line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20
status_right = GPIO.input(line_pin_right)
status_middle = GPIO.input(line_pin_middle)
status_left = GPIO.input(line_pin_left
PWMB = 23
BIN1 = 25
BIN2 = 24


def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height / 2):, :, :]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    image = cv2.GaussianBlur(image, (5, 5), 0)
    _, image = cv2.threshold(image, 160, 255, cv2.THRESH_BINARY_INV)
    image = image / 255
    return image


camera = cv2.VideoCapture(-1) # -1 ?? 0 이랑 같은듯
camera.set(3, 640)
camera.set(4, 480)


def spare_capture():
    model_path = '/home/pi/AI_CAR/model/lane_navigation_final.h5'
    model = load_model(model_path)
#model 설정
    whatspare = "None"

    try:
        while True:
            keyValue = cv2.waitKey(1) #키보드 입력대기

            _, image = camera.read() #_은 읽기 성공여부, true or false
            image = cv2.flip(image, -1) # 양수 = 좌우대칭, 0 = 상하대칭 , 음수 = 모두수행
            preprocessed = img_preprocess(image)
            cv2.imshow('pre', preprocessed) # 'pre' = 창제목 으로 창 띄워 보여주기
            X = np.asarray([preprocessed])
            whatspare = int(model.predict(X)[0])
            print("spare is:", whatspare)

            if whatspare == "nozzle_1":
                print("Nozzle 1pcs") # GUI로 보내기
            elif whatspare == "nozzle_2":
                print("Nozzle 2pcs") # GUI로 보내기
            elif whatspare == "nozzle_3":
                print("Nozzle 3pcs") # GUI로 보내기
            elif whatspare == "pump_1":
                print("Pump 1pcs") # GUI로 보내기
            elif whatspare == "pump_2":
                print("Pump 2pcs") # GUI로 보내기
            elif whatspare == "pump_3":
                print("Pump 3pcs") # GUI로 보내기
            else :
                print("unknown")

    except KeyboardInterrupt:
        pass

# 여기서 부터는 Tracking line

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(line_pin_right, GPIO.IN)
    GPIO.setup(line_pin_middle, GPIO.IN)
    GPIO.setup(line_pin_left, GPIO.IN)
    # motor.setup()


def T_L():
    # print('R%d   M%d   L%d'%(status_right,status_middle,status_left))
    if status_middle == 0 and status_left == 0 and status_right == 0:
        move.move(50, 'forward', 'no', 1)
    elif status_right == 1:
        move.move(50, 'forward', 'right', 0.6)
    elif status_left == 1:
        move.move(50, 'forward', 'left', 0.6)
    elif status_middle == 1 and status_left == 1 and status_right == 1:
        move.motorstop()
        spare_capture()
        time.sleep(1)
        move.move(50, 'forward', 'no', 1)
    else:
        move.move(50, 'backward', 'no', 1)

# 여기까지 Tracking line


if __name__ == '__main__':
    try:
        setup()
        move.setup()
        while 1:
            T_L()
            if status_middle == 0 and status_left == 1 and status_right == 0:
                break
        time.sleep(1)
        pass
    except KeyboardInterrupt:
        move.destroy()
