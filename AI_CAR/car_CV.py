import time
import cv2
import RPi.GPIO as GPIO
import numpy as np
from tensorflow.keras.models import load_model
from AI_CAR import move

line_pin_right = 19
line_pin_middle = 16
line_pin_left = 20
status_right = GPIO.input(line_pin_right)
status_middle = GPIO.input(line_pin_middle)
status_left = GPIO.input(line_pin_left

model = tensorflow.keras.models.load_model('keras_model.h5')  # file 집어넣기
cap = cv2.VideoCapture(0)
size = (224, 224)
classes = ['empty', 'nozzle_1', 'nozzle_1', 'nozzle_1', 'pump_1', 'pump_2', 'pump_3']

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height / 2):, :, :]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    image = cv2.GaussianBlur(image, (5, 5), 0)
    _, image = cv2.threshold(image, 160, 255, cv2.THRESH_BINARY_INV)
    image = image / 255
    return image


def spare_capture():
    model_path = '/home/pi/AI_CAR/model/lane_navigation_final.h5'
    model = load_model(model_path)
#model 설정
    whatspare = "None"

    try:
        # keyValue = cv2.waitKey(1) #키보드 입력대기
        ret, img = cap.read()
        h, w, _ = img.shape
        cx = h / 2
        img = img[:, 200:200 + img.shape[0]]
        img = cv2.flip(img, 1)

        img_input = cv2.resize(img, size)
        img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
        img_input = (img_input.astype(np.float32) / 127.0) - 1
        img_input = np.expand_dims(img_input, axis=0)
        cv2.imshow('pre', img_input) # 'pre' = 창제목 으로 창 띄워 보여주기
        prediction = model.predict(img_input)
        idx = np.argmax(prediction)

        whatspare = int(classes[idx])
        print("spare is:", whatspare)
        if whatspare == "empty":
            print("empty") # GUI로 보내기
        elif whatspare == "nozzle_1":
            print("Nozzle 1pcs")  # GUI로 보내기
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

            while carState == "go":
                if steering_angle >= 70 and steering_angle <= 110:
                    print("go")
                    move.move(50, 'forward', 'no', 1)
                elif steering_angle > 111:
                    print("right")
                    move.move(50, 'forward', 'right', 0.6)
                elif steering_angle < 71:
                    print("left")
                    move.move(50, 'forward', 'left', 0.6)
                if carState == "capture_stop":
                    move.motorStop()
                    time.sleep(1)
                    spare_capture()
                    time.sleep(1)
                    continue
                if carState == "stop":
                    move.motorStop()
                    break
            if carState == "stop":
                move.motorStop()
                ##### 여기서 다시 carstate = go 로 반환하는구문 추가

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()