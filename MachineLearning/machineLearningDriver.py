from readData import getData, getLiveData
from modelGenerator import generateModel
from liveTool import showModel


def generateModelFromImages():
    #getData(CSV_NAME)
    getLiveData(CSV_NAME, LABEL_LIST)
    generateModel(CSV_NAME, MODEL_FILE)


CSV_NAME = 'DataBCPI.csv'
MODEL_FILE = 'DataModel.pkl'
LABEL_LIST = ['B','C']

generateModelFromImages()
showModel(MODEL_FILE)
