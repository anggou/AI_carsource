import threading
import time
import cv2
import RPi.GPIO as GPIO
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import move
#검은차를 직접 움직이면서, 순간순간 스페어 몇개인지 인식

size = (224, 224)
classes = ['nozzle_1', 'nozzle_1', 'nozzle_1', 'pump_1', 'pump_2', 'pump_3']

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20
status_right = GPIO.input(line_pin_right)
status_middle = GPIO.input(line_pin_middle)
status_left = GPIO.input(line_pin_left)

camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)

def spare_capture():
    model_path = '/home/pi/AI_CAR/model/lane_navigation_final.h5'
    model = load_model(model_path)
#model 설정
    whatspare = "None"

    try:
        while camera.isOpened():  # 초기화
            model = tensorflow.keras.models.load_model('keras_model_spare.h5')  # file 집어넣기
            ret, img = camera.read()
            if not ret:
                break

            h, w, _ = img.shape
            cx = h / 2
            img = img[:, 200:200 + img.shape[0]]
            img = cv2.flip(img, 1)

            img_input = cv2.resize(img, size)
            img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
            img_input = (img_input.astype(np.float32) / 127.0) - 1
            img_input = np.expand_dims(img_input, axis=0)

            prediction = model.predict(img_input)
            idx = np.argmax(prediction)
            whatspare = int(classes[idx])
            print("spare is:", whatspare)

            if whatspare == 'nozzle_1':
                print("Nozzle 1pcs") # GUI로 보내기
            elif whatspare == 'nozzle_2':
                print("Nozzle 2pcs") # GUI로 보내기
            elif whatspare == 'nozzle_3':
                print("Nozzle 3pcs") # GUI로 보내기
            elif whatspare == 'pump_1':
                print("Pump 1pcs") # GUI로 보내기
            elif whatspare == 'pump_2':
                print("Pump 2pcs") # GUI로 보내기
            elif whatspare == 'pump_3':
                print("Pump 3pcs") # GUI로 보내기
            else :
                print("unknown")

    except KeyboardInterrupt:
        pass

def main():
    try:
        while True:
            keyValue = cv2.waitKey(1)
            if keyValue == ord('q'):
                break
            elif keyValue == 82:
                print("go")
                move.move(50, 'forward', 'no', 1)
            elif keyValue == 84:
                print("stop")
                move.motorStop()
            elif keyValue == 81:
                print("left")
                move.move(50, 'forward', 'left', 0.6)
            elif keyValue == 83:
                print("right")
                move.move(50, 'forward', 'right', 0.6)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()
    GPIO.cleanup()
