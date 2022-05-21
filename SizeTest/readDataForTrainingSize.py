import pickle
import sys
import time
import warnings

import cv2
import numpy as np
import mediapipe as mp
from library import fixateList, list_ports
import pandas as pd
import os


def getSizeTestData(model_file):
    index = 0
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
        selectedDriver = list_ports()
        if str(selectedDriver) == "ERROR! Could not match input with available Driver":
            print(selectedDriver)
            sys.exit()
        cap = cv2.VideoCapture(selectedDriver)
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        mpDraw = mp.solutions.drawing_utils

        cv2.waitKey(1)
        while True:
            img = cv2.flip(cap.read()[1],1)
            imageToSafe = img
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            currentGesture = []

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        currentGesture.append([cx,cy])

            cv2.imshow('Webcam', img)

            if cv2.waitKey(1) & 0xFF == ord(' '):
                if len(currentGesture)==21:
                    path = os.getcwd() + "\\SizeTestData\\"
                    print("Saved")
                    cv2.imwrite(f'{path}img{index}.jpg', imageToSafe)
                    index += 1

        cap.release()
        cv2.destroyAllWindows()
        cv2.destroyAllWindows()

getSizeTestData('../DataModel.pkl')
