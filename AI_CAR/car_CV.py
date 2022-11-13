import threading
import time
import cv2
import RPi.GPIO as GPIO
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import move

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20
status_right = GPIO.input(line_pin_right)
status_middle = GPIO.input(line_pin_middle)
status_left = GPIO.input(line_pin_left

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

def main():
    model_path = '/home/pi/AI_CAR/model/lane_navigation_final.h5'
    model = load_model(model_path)
    carState = "stop"

    try:
        while True:
            keyValue = cv2.waitKey(1)

            if keyValue == ord('q'):
                break
            elif keyValue == 82:
                print("go")
                carState = "go"
            elif keyValue == 84:
                print("stop")
                carState = "stop"
            elif status_middle == 1 and status_left == 1 and status_right == 1:
                carState = "capture_stop"

            _, image = camera.read()
            image = cv2.flip(image, -1)
            preprocessed = img_preprocess(image)
            cv2.imshow('pre', preprocessed)

            X = np.asarray([preprocessed])
            steering_angle = int(model.predict(X)[0])
            print("predict angle:", steering_angle)

            if carState == "go":
                if steering_angle >= 70 and steering_angle <= 110:
                    print("go")
                    move.move(50, 'forward', 'no', 1)
                elif steering_angle > 111:
                    print("right")
                    move.move(50, 'forward', 'right', 0.6)
                elif steering_angle < 71:
                    print("left")
                    move.move(50, 'forward', 'left', 0.6)
            elif carState == "stop":
                move.motorStop()
            elif carState == "capture_stop":
                move.motorStop()
                time.sleep(1)
                spare_capture()
                time.sleep(1)
                ##### 여기서 다시 carstate = go 로 반환하는구문 추가

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()