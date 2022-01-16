import csv
import ctypes
import os
import sys
import time

import cv2
import mediapipe as mp
import numpy as np
from library import list_ports, fixateList


def getData(csvname):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils


    landmarks = ['class']
    num_coords = 21
    for val in range(1, num_coords+1):
        landmarks += ['x{}'.format(val), 'y{}'.format(val)]

    with open(csvname, mode='w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(tuple(landmarks))


    for folder in os.listdir(os.getcwd() + "\data\\"):
        class_name = folder
        path = os.getcwd() + "\data\\" + folder + "\\"
        for filename in os.listdir(path):
            name, file_extension = os.path.splitext(filename)
            if '.jpeg' or '.jpg' in file_extension:
                img = cv2.flip(cv2.imread(path + filename), 1)
                #cv2.imshow("Image", hand)
                imgRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                results = hands.process(imgRGB)

                currentGesture = []

                if results.multi_hand_landmarks:
                    for handLms in results.multi_hand_landmarks:
                        for id, lm in enumerate(handLms.landmark):
                            h, w, c = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            currentGesture.append([cx,cy])

                if len(currentGesture)==21:
                    currentGesture = fixateList(currentGesture)
                    row = list(np.array([[gest[0], gest[1]] for gest in currentGesture]).flatten())
                    row.insert(0, class_name)

                    # Export to CSV
                    with open(csvname, mode='a', newline='') as f:
                        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(tuple(row))


def getLiveData(csvname, label_list):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils


    landmarks = ['class']
    num_coords = 21
    for val in range(1, num_coords+1):
        landmarks += ['x{}'.format(val), 'y{}'.format(val)]

    with open(csvname, mode='w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(tuple(landmarks))


    def Mbox(title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    Mbox('Hinweis', 'Oben Links wird die zu zeigende Geste gezeigt. Per Leertaste werden die Aufzeichnungen begonnen.', 0)


    picturesToTake = 1000
    handList = ['Rechts ', 'Links ']
    cv2.waitKey(1)
    selectedDriver = list_ports()
    cap = cv2.VideoCapture(selectedDriver)
    if str(selectedDriver) == "ERROR! Could not match input with available Driver":
        print(selectedDriver)
        sys.exit()
    for label in label_list:
        for currentHand in handList:
            index = 0

            while True:
                success, img = cap.read()
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = hands.process(imgRGB)

                if results.multi_hand_landmarks:
                    for handLms in results.multi_hand_landmarks:
                        for id, lm in enumerate(handLms.landmark):
                            h, w, c = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                cv2.putText(img, currentHand + label, (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 255), 3)


                cv2.imshow("Vorschaubild", img)
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    break

            cv2.destroyAllWindows()
            while index < picturesToTake:
                success, img = cap.read()
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = hands.process(imgRGB)

                currentGesture = []

                if results.multi_hand_landmarks:
                    for handLms in results.multi_hand_landmarks:
                        for id, lm in enumerate(handLms.landmark):
                            h, w, c = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            currentGesture.append([cx,cy])

                cv2.putText(img, str(int(picturesToTake-index)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)
                cv2.imshow("Aufnahme", img)
                cv2.waitKey(1)
                if len(currentGesture)==21:
                    index += 1
                    currentGesture = fixateList(currentGesture)
                    row = list(np.array([[gest[0], gest[1]] for gest in currentGesture]).flatten())
                    row.insert(0, label)

                    # Export to CSV
                    with open(csvname, mode='a', newline='') as f:
                        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        csv_writer.writerow(tuple(row))

            cv2.destroyAllWindows()
