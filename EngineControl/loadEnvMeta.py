import json, EnviroObject, Enemy, os


from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler

DefaultTransTilePos = {
    "UP": [1490, 10],
    "DOWN": [1490, 990],
    "LEFT": [-50, 490],
    "RIGHT":[3000, 490]
}

def getFlipbookPath(name, package=None):
    if package == None:
        pass
    return "EngineControl\\GamePlayObjects\\FlipBooks\\" + name + ".flip"



def loadEnv(fileName):
    filePath = fileName

    scanMetaFile = open(filePath)
    retVal = json.loads(scanMetaFile.read())
    scanMetaFile.close()
    return retVal

def objectTable():
    envObjTypes = {
            "EnvColorObj": EnviroObject.InstColorObj,
            "EnvColorBg": EnviroObject.InstColorBg,
            "EnvColorPlat": EnviroObject.InstColorPlat,
            "EnvImageObj": EnviroObject.InstImageObj,
            "EnvShuffleImageObj": EnviroObject.InstShuffleImageObj,
            "EnvShuffleImageBg": EnviroObject.InstShuffleImageBg,
            "EnvShuffleImagePlat": EnviroObject.InstShuffleImagePlat,
            "EnvAnimImageObj": EnviroObject.InstAnimImageObj,
            "EnvAnimImageBg": EnviroObject.InstAnimImageBg,
            "EnvAnimImagePlat": EnviroObject.InstAnimImagePlat,
            "EnvImageGridObj": EnviroObject.InstImageGridObj,
            "EnvImageGridBg": EnviroObject.InstImageGridBg,
            "EnvImageGridPlat": EnviroObject.InstImageGridPlat,
            "EnvImageBg": EnviroObject.InstImageBg,
            "EnvImagePlat": EnviroObject.InstImagePlat,
            "ImageObject": EnviroObject.InstSingleImageObj,
            "ImageObj": EnviroObject.InstSingleImageObj,
            "ImageBg": EnviroObject.InstSingleImageBg,
            "ImagePlat": EnviroObject.InstSingleImagePlat
        }
    return envObjTypes

def enemyTable():
    enemyObjTypes = {}
    return enemyObjTypes

def getEvlJsonPath(Plane, Grid):
    gridFileName = str(Grid[0]) + "_" + str(Grid[1]) + ".json"
    return "\\".join(["EnvironmentData", Plane, gridFileName])


def doesNextLevelExist(Plane, Grid, Next):
    myGrid = Grid[:]
    if Next == "UP":
        myGrid[1] -= 1

    elif Next == "DOWN":
        myGrid[1] += 1

    elif Next == "LEFT":
        myGrid[0] -= 1

    elif Next == "RIGHT":
        myGrid[0] += 1

    # print getEvlJsonPath(Plane, myGrid)
    return os.path.isfile(getEvlJsonPath(Plane, myGrid))








# Level Editor Stuff
def loadTemplate(type, name, fileName="WorldTemplates.json"):
    filePath = "EngineControl\\EditorData\\" + fileName

    scanMetaFile = open(filePath)
    retVal = json.loads(scanMetaFile.read())
    scanMetaFile.close()
    return retVal[type][name]


def saveTemplates(Dict):
    filePath = "EngineControl\\EditorData\\WorldTemplates.json"

    scanMetaFile = open(filePath, "w")
    scanMetaFile.write(json.dumps(Dict, sort_keys=True, indent = 4, separators = (',', ': ')))

    scanMetaFile.close()

def saveEnvPath(filePath, Dict):

    scanMetaFile = open(filePath, "w")
    scanMetaFile.write(json.dumps(Dict, sort_keys=True, indent = 4, separators = (',', ': ')))

    scanMetaFile.close()

def saveEnv(fileName, Dict):
    filePath = "\\".join(["EnvironmentData", fileName])


    scanMetaFile = open(filePath, "w")
    scanMetaFile.write(json.dumps(Dict, sort_keys=True, indent = 4, separators = (',', ': ')))

    scanMetaFile.close()