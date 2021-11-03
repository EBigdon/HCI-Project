import sys

import cv2
import mediapipe as mp
import time

def list_ports():
    dev_port = 0
    ports = []
    while True:
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            break
        else:
            is_reading, img = camera.read()
            if is_reading:
                ports.append(dev_port)
        dev_port +=1
    cv2.waitKey(1)
    print(f"Found {len(ports)} camera-drivers.\n Please select your driver:\n {ports}.")
    selected = int(input())
    for i in ports:
        if selected == i:
            return selected
        else:
            return "ERROR! Could not match input with available Driver"


def get_right_camera(list_of_drivers): #Zeige alle Bilder und frag ab ob richtig
    if len(list_of_drivers) == 1:#Change to 1 later!
        return list_of_drivers[0]
    else:
        for i in list_of_drivers:
            #Hier muss öffnen der Camera hin und Abfragefenster, ob richtig, wenn ja schließe Kamera und gib i zurück, sonst schließe Kamera und gehe weiter in for-Schleife
            print(f"Selected Driver: {i}")
            cap = cv2.VideoCapture(i)
            while True:
                success, img = cap.read()
                cv2.imshow("Image", img)
                if cv2.waitKey(1) & 0xFF == ord(' '):
                    break


#cap = cv2.VideoCapture(get_right_camera(list_ports()))
selectedDriver = list_ports()
if str(selectedDriver) == "ERROR! Could not match input with available Driver":
    print(selectedDriver)
    sys.exit()
cap = cv2.VideoCapture(selectedDriver)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
isRightCamera = None
cv2.waitKey(1)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)
                # if id == 4:
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
        
cap.release()
cv2.destroyAllWindows()
