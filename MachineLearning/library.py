import cv2
import sys

def fixateList(list):
    value1 = list[0][0]
    value2 = list[0][1]
    for indx, i in enumerate(list):
        list[indx][0] = list[indx][0] - value1
        list[indx][1] = list[indx][1] - value2
    return list


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
        if len(ports) == 0:
            print('Kein Treiber gefunden! Bitte Kamera überprüfen.')
            sys.exit()
        else:
            print(f"Found {len(ports)} camera-drivers.\n Please select your driver:\n {ports}.")
            selected = int(input())
            for i in ports:
                if selected == i:
                    return selected
                else:
                    return "ERROR! Could not match input with available Driver"
