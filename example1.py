import cv2
import time
import math
import numpy as np
from mtcnn import MTCNN


def main():
    detector = MTCNN()  # deklaracja detektora

    cap = cv2.VideoCapture(0)
    while True:
        ret, image = cap.read()
        if not ret:
            raise IOError("webcam failure")
        if image is not None:

            t = time.time()
            result = detector.detect_faces(image)  # predykcja

            right_eye_x = result[0]['keypoints']['right_eye'][0]
            right_eye_y = result[0]['keypoints']['right_eye'][1]
            left_eye_x = result[0]['keypoints']['left_eye'][0]
            left_eye_y = result[0]['keypoints']['left_eye'][1]

            right_eye = (right_eye_x, right_eye_y)
            left_eye = (left_eye_x, left_eye_y)
            point = (right_eye_x, left_eye_y)

            if left_eye_x - right_eye_x != 0:
                angle = np.degrees(math.atan((left_eye_y - right_eye_y) / (left_eye_x - right_eye_x)))

            for face in result:
                # confidence = face["confidence"]
                # color = (0, int(255*confidence), 0)
                x = face["box"][0]
                y = face["box"][1]
                width = face["box"][2]
                height = face["box"][3]
                if result[0]['confidence'] >= 0.995:
                    cv2.rectangle(image, (x, y), (x + width, y + height), (0, 0, 255), 2)
                    for keypoint in face["keypoints"].values():
                        cv2.circle(image, keypoint, 2, (0, 0, 255), -1)
                else:
                    cv2.rectangle(image, (x, y), (x + width, y + height), (255, 255, 255), 2)
                    for keypoint in face["keypoints"].values():
                        cv2.circle(image, keypoint, 2, (255, 255, 255), -1)

            if -5 < angle < 5:
                print("GLOWA BEZ ROTACJI, kąt: ", angle)
                image = cv2.putText(img=image, text='GLOWA BEZ ROTACJI', org=(0, 50),
                                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                                    color=(0, 0, 255), thickness=1)
                image = cv2.putText(img=image, text=str(angle), org=(0, 100),
                                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                                    color=(0, 0, 255), thickness=1)
            if 5 < angle:
                print("OBRÓT W LEWO, kąt: ", angle)
                image = cv2.putText(img=image, text='OBROT W LEWO', org=(0, 50),
                                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                                    color=(0, 0, 255), thickness=1)
                image = cv2.putText(img=image, text=str(angle), org=(0, 100),
                                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                                    color=(0, 0, 255), thickness=1)
            if -5 > angle:
                print("OBRÓT W PRAWO, kąt: ", angle)
                image = cv2.putText(img=image, text='OBROT W PRAWO', org=(0, 50),
                                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                                    color=(0, 0, 255), thickness=1)
                image = cv2.putText(img=image, text=str(angle), org=(0, 100),
                                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1,
                                    color=(0, 0, 255), thickness=1)

            czas = time.time() - t
            print('Czas: ', czas)

            cv2.imshow("Output", image)
            print(result)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()