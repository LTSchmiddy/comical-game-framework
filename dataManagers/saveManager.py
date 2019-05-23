import os, runpy

class SaveManager:
    def __init__(self):

        self.isGameFileLoaded = False

        self.showLoadMenu = False

        self.shouldSave = False
        self.shouldLoad = False
        self.shouldNew = False

        self.savePath = "gameSaves\save1.cgs"


    def DisplayLoadMenu(self):
        self.showLoadMenu = True

    def save(self):
        self.shouldSave = True

    def load(self):
        self.isGameFileLoaded = True
        self.shouldLoad = True

    def newGame(self):
        self.isGameFileLoaded = True
        self.shouldNew = True

    def getSaveTrigger(self):
        if self.shouldSave:
            self.shouldSave = False
            return True
        else:
            return False

    def getLoadTrigger(self):
        if self.shouldLoad:
            self.shouldLoad = False
            return True
        else:
            return False


    def getNewTrigger(self):
        if self.shouldNew:
            self.shouldNew = False
            return True
        else:
            return False


