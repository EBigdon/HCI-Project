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


def showModel(model_file):
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
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            currentGesture = []

            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id, lm in enumerate(handLms.landmark):
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        currentGesture.append([cx,cy])
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            if len(currentGesture)==21:
                currentGesture = fixateList(currentGesture)
                row = list(np.array([[gest[0], gest[1]] for gest in currentGesture]).flatten())
                warnings.simplefilter("ignore")
                X = pd.DataFrame([row])
                body_language_class = model.predict(X)[0]
                body_language_prob = model.predict_proba(X)[0]
                for prob in body_language_prob:
                    if prob > 0.75: #IsThisAGoodValue
                        #cv2.putText(img, (str(body_language_class) + " | " + str(body_language_prob)),(10, 50), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 255), 2)
                        cv2.putText(img, str(body_language_class),(10, 50), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 255), 2)
                #print(str(body_language_class) + " | " + str(body_language_prob))

            cv2.imshow('Webcam', img)

            if cv2.waitKey(1) & 0xFF == ord(' '):
                break

        cap.release()
        cv2.destroyAllWindows()
        cv2.destroyAllWindows()
