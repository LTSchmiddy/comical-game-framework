import os, json

defaultControlPath = "gameSettings.json"
controlPath = "gameSettings.json"



# print os.path.isfile(controlPath)

def getSettingsDict(inPath = controlPath):
    # import json


    scanMetaFile = open(inPath)
    retVal = json.loads(scanMetaFile.read())
    scanMetaFile.close()

    return retVal

def setSettingsDict(dataOut):
    global controlPath

    scanMetaOut = open(controlPath, 'w')
    json.dump(dataOut, scanMetaOut, indent=4, sort_keys=True)
    scanMetaOut.close()


def getScreenSettings(fileName):
    scanMetaFile = open("ScreenConfigs\\" + fileName + ".json")
    retVal = json.loads(scanMetaFile.read())
    scanMetaFile.close()

    return retVal