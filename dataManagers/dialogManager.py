import os, runpy

class dialogManager:
    def __init__(self):

        self.dialogPath = ""
        self.host = None

        self.imagePath = ""



    def trigger(self, dialogID, host=None):
        self.dialogPath = "EngineControl\\GamePlayObjects\\Conversations\\" + dialogID + ".dialog"
        self.host = host

    def getDialog(self):
        if self.dialogPath != "":
            runVal = runpy.run_path(self.dialogPath)
            self.dialogPath = ""
            runVal["host"] = self.host
            return runVal
        else:
            return None


    def triggerImage(self, imagePath):
        self.imagePath = imagePath


    def getImage(self):
        retVal = self.imagePath
        self.imagePath = ""

        return retVal



# class dialogBGManager:
#     def __init__(self):
#
#         self.imagePath = ""
#
#
#
#     def trigger(self, imagePath, host=None):
#         self.imagePath = imagePath
#         self.host = host
#
#     def getImage(self):
#         retVal = self.imagePath
#         self.imagePath = ""
#
#         return retVal


