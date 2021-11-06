import sys

import cv2
import mediapipe as mp
import time


def checkForSimilarities(inputedGesture):
    alphabet = [
        [["C"], [0, 0], [31, -83], [38, -84], [40, -2], [46, -82], [50, -112], [54, -75], [54, -120], [62, -115], [66, -20], [68, -101], [71, -121], [78, -128], [83, -33], [83, -126], [84, -114], [90, -123], [98, -48], [99, -128], [100, -121], [101, -127]],
        [["B"],[0, 0], [2, 97], [2, 25], [3, 53], [26, -28], [27, 216], [28, 83], [29, 30], [29, -2], [48, -45], [52, 78], [53, -16], [55, 21], [70, 91], [74, 194], [74, -30], [79, 82], [79, -2], [82, 30], [99, 109], [104, 149]]
    ]
    found = False
    index = 0
    try:
        for letter in alphabet:
            if found:
                break
            index = 1
            for line in inputedGesture:
                #print(f"1: {line[1]} and 2: {line[2]}")
                if (letter[index])[0]-25 <= line[1] <= (letter[index])[0]+25:
                    if (letter[index])[1]-25 <= line[2] <= (letter[index])[1]+25:
                        if index == len(inputedGesture)-1:
                            print((letter[0])[0], end="")
                            found = True
                else:
                    break
                index += 1
    except:
        print("", end="")


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
    cv2.waitKey(2)
    if len(ports) == 1:
        print(f"Found 1 camera-driver. Camera-driver {ports[0]} gets selected.")
        return ports[0]
    else:
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


def quickSort(list):
    if not list:
        return list
    pivot = list[0]
    lesser = quickSort([x for x in list[1:] if x[1] < pivot[1]])
    greater = quickSort([x for x in list[1:] if x[1] >= pivot[1]])
    return lesser + [pivot] + greater


def fixateList(list):
    value1 = list[0][1]
    value2 = list[0][2]
    for indx, i in enumerate(list):
        list[indx][1] = list[indx][1] - value1
        list[indx][2] = list[indx][2] - value2
    return list

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
cv2.waitKey(1)

handGesture = []

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    toSort = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                toSort.append([id,cx,cy])
                #print(id, cx, cy)
                # if id == 4:
                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if len(toSort)>0:
        toSort = fixateList(quickSort(toSort))
        handGesture.append(toSort)
        checkForSimilarities(toSort)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break
for line in handGesture:
    print(line)
cap.release()
cv2.destroyAllWindows()
