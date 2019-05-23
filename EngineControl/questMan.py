import os, runpy, pickle
from EngineControl import GameStat

class QuestManager:
    def __init__(self, world):
        self.questDir = "EngineControl\\GamePlayObjects\\QuestFiles"
        self.questTable = {}

    def loadNewQuest(self, questFile):
        filePath = self.questDir + "\\" + questFile
        cModDict = runpy.run_path(filePath)
        self.questTable[cModDict["questID"]] = Quest(self.world, cModDict)



class Quest:
    def __init__(self, world, questDict):
        self.world = world
        self.fileDict = questDict

        self.ID = questDict["questID"]
        self.name = questDict["name"]
        self.variables = questDict["questVariables"]
        self.descFn = questDict["GetJournalDesc"]

    def getQuestDescription(self):
        return self.descFn(self.world, self.variables)
