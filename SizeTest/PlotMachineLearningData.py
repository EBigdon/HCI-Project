import csv

import matplotlib.pyplot as plt
from csv import reader

from Holistic.SizeTest.TestWithData import checkTestData
from Holistic.modelGenerator import generateModel


def plotGraph():
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.title("Line graph")
    plt.plot(x, color="red")
    plt.show()

#x = np.array()
#x = np.append(x,0.5)
x = [0]
#plotGraph()

e = 1
startValue = 1
anzGestures = 1000
while (e <= anzGestures):
    if e > startValue:
        gestures = 4
        gesturesToCheck = 4
        hands = 2
        handsToCheck = 2
        gesturesPerHand = 1000
        listOfGesturesToCheck = []
        i = 0
        while (i < gestures):
            if (i < gesturesToCheck):
                j = 0
                while (j < hands):
                    if (j < handsToCheck):
                        k = 0
                        while (k < gesturesPerHand):
                            #print(k + gesturesPerHand * ((j) + (i)) + i * gesturesPerHand)
                            if(k < e):
                                listOfGesturesToCheck.append(k + gesturesPerHand * ((j) + (i)) + i * gesturesPerHand)
                            k += 1
                    else :
                        j += 1
                    j += 1
            else:
                i += 1
            i += 1
        index = 0
        result = []
        headline = ""
        with open('../DataBCPI.csv', 'r') as read_obj:
            if index in listOfGesturesToCheck:
                csv_reader = reader(read_obj)
                for row in csv_reader:
                    if index - 1 in listOfGesturesToCheck:
                        result.append(row)
                    if index - 1 == -1:
                        headline = row
                    index += 1

        with open('../Data.csv', mode='w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(tuple(headline))
            for row in result:
                csv_writer.writerow(tuple(row))

        if e != 1:
            print(e)
            generateModel('../Data.csv', 'test_training_model.pkl')
            x.append(checkTestData('test_training_model.pkl'))
    e += 1

x.pop(0)
x.append(checkTestData('../test_model.pkl'))
plotGraph()
