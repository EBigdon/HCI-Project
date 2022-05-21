import os
import pickle
import warnings

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

from Holistic.library import fixateList

def checkTestData(model_file):
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
        path = os.getcwd() + "\\SizeTestData\\"
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        score = 0
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
                    warnings.simplefilter("ignore")
                    X = pd.DataFrame([row])
                    body_language_class = model.predict(X)[0]
                    body_language_prob = model.predict_proba(X)[0]
                    fileNum = name.split("img")[1]
                    if int(fileNum) < 10:
                        #print(f"Pred:{body_language_class}|B")
                        if body_language_class == "B":
                            score += 1
                    else:
                        #print(f"Pred:{body_language_class}|C")
                        if body_language_class == "C":
                            score += 1
    #print(score/20)
    endscore = score/20
    return endscore
