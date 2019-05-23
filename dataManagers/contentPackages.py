import pygame, zipfile, os, json, runpy
from cStringIO import StringIO

packageDirectories = ["EngineControl/ContPacks"]




class ContentPackageHandler:
    def __init__(self, autoload = True):
        global packageDirectories
        self.packageDirectories = packageDirectories

        self.packDict = {}

        if autoload:
            self.loadContentPacks()

    def getPackage(self, packageName):
        return self.packDict[packageName]


    def loadInterMod(self, worldobj, imodPath, packageID = None):
        if packageID == None:
            if not imodPath.startswith("@"):
                return runpy.run_path("EngineControl\\GamePlayObjects\\InteractionModules\\" + imodPath + ".inter")["InterMod"](worldobj)
            else:
                packageName = imodPath.split(":")[0][1:]
                locationInPackage = imodPath.split(":")[1]


            return self.getPackage(packageName).getInterMod(locationInPackage)
        else:
            return self.getPackage(packageID).getInterMod(imodPath)
        
        
        
    def loadImage(self, imagePath, packageID = None):
        if packageID == None:
            if not imagePath.startswith("@"):
                return pygame.image.load(imagePath)
            else:
                packageName = imagePath.split(":")[0][1:]
                locationInPackage = imagePath.split(":")[1]
                # print packageName

            # imageData = StringIO(self.getPackage(packageName).read(locationInPackage))
            # return pygame.image.load(imageData)
            return self.getPackage(packageName).getImage(locationInPackage)
        else:
            return self.getPackage(packageID).getImage(imagePath)


    def loadContentPacks(self):
        for dir in self.packageDirectories:
            self.loadFromDir(dir)

    def loadFromDir(self, dir):

        for i in os.listdir(dir):
            # print i
            if i.endswith(".zip") or i.endswith(".cpk"):
                dirPath = dir + "/" + i
                # print dirPath, "-"
                newArch = zipfile.ZipFile(dirPath)
                # print newArch.namelist()

                if not ("PackageInfo.json" in newArch.namelist()):
                    print "Content Package", dirPath, "is missing PackageInfo.json at at archive root. This package is invalid and will not be loaded."
                else:

                    self.packDict[json.loads(newArch.open("PackageInfo.json").read())["ID"]] = ContentPackage(newArch)


            elif os.path.isdir(dir + "/" + i):
                self.loadFromDir(dir + "/" + i)


            # print self.packDict["EXP1"].packageInfo


    def getRunPyDict(self, file, pack):
        pass


class ContentPackage:
    def __init__(self, zipArchive):
        self.archive = zipArchive
        self.packageInfo = json.loads(self.archive.open("PackageInfo.json").read())
        self.packageID = self.packageInfo["ID"]

        self.itemDicts = {}
        self.projDicts = {}
        self.loadAllDicts()

        # print self.itemDicts


    def loadAllDicts(self, dictList = [".item", ".proj"]):
        for i in self.archive.namelist():

            if (i.endswith(".item")) and (".item" in dictList):
                newItem = self.getItemDict(i)
                self.itemDicts[newItem["itemID"]] = newItem

            if (i.endswith(".proj")) and (".proj" in dictList):
                newProj = self.getProjDict(i)
                self.projDicts[newProj["ID"]] = newProj



    def getImage(self, imageLocation):
        return pygame.image.load(StringIO(self.archive.read(imageLocation)))



    def getInterMod(self, imodLocation):
        tempPath = "EngineControl/TempFiles/itemImterFile.inter"

        tempFile = open(tempPath, "w")
        itemString = self.archive.open(imodLocation + ".inter").read()

        # Make Tweaks Here...

        itemString = self.packageID.join(itemString.split("*this*"))

        tempFile.write(itemString)
        tempFile.close()

        return runpy.run_path(tempPath + ".inter")["InterMod"](self)



    def getItemDict(self, itemFile):
        tempPath = "EngineControl/TempFiles/itemTempFile.item"

        tempFile = open(tempPath, "w")
        itemString = self.archive.open(itemFile).read()

        # Make Tweaks Here...

        itemString = self.packageID.join(itemString.split("*this*"))

        tempFile.write(itemString)
        tempFile.close()

        retDict = runpy.run_path(tempPath)

        if not "forceNative" in self.packageInfo:
            retDict["itemID"] = self.packageID + "." + retDict["itemID"]
        else:
            if self.packageInfo["forceNative"] == False:
                retDict["itemID"] = self.packageID + "." + retDict["itemID"]

        return retDict



    def getProjDict(self, projFile):
        tempPath = "EngineControl/TempFiles/projTempFile.proj"

        tempFile = open(tempPath, "w")
        projString = self.archive.open(projFile).read()

        # Make Tweaks Here...

        projString = self.packageID.join(projString.split("*this*"))

        tempFile.write(projString)
        tempFile.close()

        retDict = runpy.run_path(tempPath)

        if not "forceNative" in self.packageInfo:
            retDict["ID"] = self.packageID + "." + retDict["ID"]
        else:
            if self.packageInfo["forceNative"] == False:
                retDict["ID"] = self.packageID + "." + retDict["ID"]

        return retDict


mainHandler = ContentPackageHandler()