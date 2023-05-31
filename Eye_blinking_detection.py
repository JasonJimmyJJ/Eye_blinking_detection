# %%
import cv2
import numpy as np
import dlib
from math import hypot
from matplotlib import pyplot as plt

# %%
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

font = cv2.FONT_HERSHEY_PLAIN

max_ratio = 5
min_ratio = 4

x_cor = []
y_cor = []
y_cor_2 = []
i = 0
start_time = 0
blink_num = 0
half_blink_num = 0
plt.ion()


def midpont(p1, p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)


def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)

    center_top = midpont(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpont(facial_landmarks.part(eye_points[4]), facial_landmarks.part(eye_points[5]))

    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_length = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_length = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    length = int(abs(left_point[0]-right_point[0]))

    eye_area = cv2.rectangle(frame, (left_point[0], int(left_point[1]-hor_line_length/3)),
                             (right_point[0], int(right_point[1]+hor_line_length/3)), (0, 255, 0), 2)

    ratio = hor_line_length / ver_line_length
    return ratio


while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        start_time += 1

        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
        landmarks = predictor(gray, face)

        # x1_eye = landmarks.part(36).x
        # x2_eye = landmarks.part(39).x
        #
        # y = landmarks.part(36).y
        # cv2.circle(frame, (x, y), 3, (0, 0, 255), 2)

        # Get both eyes ratio
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)

        # the average ratio
        blinking_ratio = (left_eye_ratio+right_eye_ratio)/2

        if 50 < start_time < 200:
            text0 = 'please look at it'
            cv2.putText(frame, text0, (100, 80), font, 3, (0, 0, 255), 3)
            hor_line = cv2.line(frame, (700, 150), (800, 150), (0, 0, 255), 2)
            ver_line = cv2.line(frame, (750, 100), (750, 200), (0, 0, 255), 2)

            # Find max and min programe
            if blinking_ratio > max_ratio:
                max_ratio = blinking_ratio

            if blinking_ratio < min_ratio:
                min_ratio = blinking_ratio

            text1 = 'max ratio is ' + str(max_ratio)[:5]
            text2 = 'min ratio is ' + str(min_ratio)[:5]
            cv2.putText(frame, text1, (50, 200), font, 1, (0, 255, 0), 3)
            cv2.putText(frame, text2, (50, 240), font, 1, (0, 255, 0), 3)

        if start_time > 220:
            i += 1
            x_cor.append(i)
            y_cor.append(blinking_ratio)
            y_cor_2.append(right_eye_ratio)

            plt.clf()

            plt.plot(x_cor, y_cor)
            # plt.plot(x_cor, y_cor_2)

            plt.pause(0.001)
            plt.ioff()  # close poloting window

            text1 = 'max ratio is ' + str(max_ratio)[:5]
            text2 = 'min ratio is ' + str(min_ratio)[:5]
            text3 = 'blinking num ' + str(blink_num)[:5]
            text4 = 'half blinking num ' + str(half_blink_num)[:5]

            if blinking_ratio > max_ratio*0.7:
                blink_num += 1

            if max_ratio*0.5 < blinking_ratio < max_ratio*0.7:
                half_blink_num +=1

            cv2.putText(frame, text1, (50, 150), font, 2, (0, 255, 0), 4)
            cv2.putText(frame, text2, (50, 200), font, 2, (0, 255, 0), 4)
            cv2.putText(frame, text3, (50, 250), font, 2, (0, 255, 0), 4)
            cv2.putText(frame, text4, (50, 300), font, 2, (0, 255, 0), 4)
            cv2.putText(frame, str(blinking_ratio), (50, 350), font, 2, (0, 255, 0), 4)

    cv2.imshow('Frame', frame)

    key = cv2.waitKey(20)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
