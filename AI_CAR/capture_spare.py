import tensorflow.keras
from AI_CAR import move
import cv2
import RPi.GPIO as GPIO

model = tensorflow.keras.models.load_model('keras_model.h5')  # file 집어넣기
cap = cv2.VideoCapture(0)
size = (224, 224)
classes = ['nozzle_1', 'nozzle_1', 'nozzle_1', 'pump_1', 'pump_2', 'pump_3']

def capture_spare():
    while cap.isOpened(): #초기화
        filepath = "/home/pi/AI_CAR/video/train"
        i = 0
        keyValue = cv2.waitKey(0)
        ret, img = cap.read()
        if not ret:
            break
        _, image = cap.read()
        image = cv2.flip(image, -1)
        cv2.imshow('Capture_camera', image)
        height, _, _ = image.shape
        save_image = image[int(height / 2):, :, :]
        cv2.imshow('Save', save_image)
        if keyValue == ord('q'):
            break
        elif keyValue == 82:
            move.move(50, 'forward', 'no', 1)
            print("go")
        elif keyValue == 84:
            move.motorStop()
            print("down")
        elif keyValue == 81:
            move.move(50, 'forward', 'left', 0.6)
            print("left")
        elif keyValue == 83:
            move.move(50, 'forward', 'right', 0.6)
            print("right")
        elif keyValue == ord('1'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 1), save_image)
            i += 1
        elif keyValue == ord('2'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 2), save_image)
            i += 1
        elif keyValue == ord('3'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 3), save_image)
            i += 1
        elif keyValue == ord('4'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 4), save_image)
            i += 1
        elif keyValue == ord('5'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 5), save_image)
            i += 1
        elif keyValue == ord('6'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 6), save_image)
            i += 1
        elif keyValue == ord('0'):
            cv2.imwrite("%s_%05d_%03d.png" % (filepath, i, 0), save_image)
            i += 1
        elif cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    capture_spare()
    cv2.destroyAllWindows()
    GPIO.cleanup()

