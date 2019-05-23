import pygame, os, pickle
from EngineControl import loadEnvMeta


class FlipbookManager:
    def __init__(self):

        self.flipbookID = ""
        self.host = None
        self.time = None



    def trigger(self, flipbookID, time=None, host=None):
        self.flipbookID = flipbookID
        self.host = host
        self.time = time


    def getFlipbook(self):
        if self.flipbookID != "":
            retVal = Flipbook(self.flipbookID)
            self.flipbookID = ""

            return retVal
        else:
            return None

    def getFlipbookID(self):
        if self.flipbookID != "":
            retVal = [self.flipbookID, self.time]
            self.flipbookID = ""
            self.time = None
            return retVal
        else:
            return None


class Flipbook:
    def __init__(self, bookName = None):

        self.book = None
        self.currentIndex = 0
        self.maxIndex = 0
        self.image = None
        self.bookName = bookName

        if self.bookName != None:
            self.loadBook()


    def loadBook(self, newBookName = None):
        if newBookName != None:
            self.bookName = newBookName

        self.book = pickle.load(open(loadEnvMeta.getFlipbookPath(self.bookName), "r"))
        self.maxIndex = len(self.book["imgList"]) - 1

    def nextImg(self):
        if self.currentIndex < self.maxIndex:
            self.currentIndex += 1
            return self.returnImage()
        else:
            return None

    def prevImg(self):
        if self.currentIndex > 0:
            self.currentIndex -= 1
            return self.returnImage()

        else:
            return None

    def isLast(self):
        if self.currentIndex == self.maxIndex:
            return True
        return False

    def isFirst(self):
        if self.currentIndex == 0:
            return True
        return False

    def returnImage(self, index = None):
        if index == None:
            index = self.currentIndex
        return pygame.image.frombuffer(self.book["imgList"][index]["image"], self.book["imgList"][index]["size"], self.book["format"])



    # These functions are mostly for editing and creating new Flipbooks:
    def newBook(self, newBookName = None):
        if newBookName != None:
            self.bookName = newBookName

        self.book = {
            "name": self.bookName,
            "format": "RGBA",
            "imgList": []
        }
        self.maxIndex = len(self.book["imgList"]) - 1

    def saveBook(self, newBookName = None):
        if newBookName != None:
            self.bookName = newBookName
        myBookFile = open(loadEnvMeta.getFlipbookPath(self.bookName), "w")
        pickle.dump(self.book, myBookFile)


    def addImage(self, imagePath, index = None):
        newImage = pygame.image.load(imagePath).convert_alpha()
        newEntry = {
            "image": pygame.image.tostring(newImage, self.book["format"]),
            "size": newImage.get_size()
        }


        if index == None:
            self.book["imgList"].append(newEntry)
        else:
            self.book["imgList"].insert(index, newEntry)

        self.maxIndex = len(self.book["imgList"]) - 1

    def addFromDir(self, folder, extension = ".png"):
        for i in range(0, len(os.listdir(folder))):
            path = folder + "\\" + str(i + 1) + extension
            self.addImage(path)

    def removeImage(self, index):
        del self.book["imgList"][index]
        self.maxIndex = len(self.book["imgList"]) - 1

    def moveImage(self, imageIndex, newIndex):
        self.book["imgList"].insert(newIndex, self.book["imgList"].pop(imageIndex))
        self.maxIndex = len(self.book["imgList"]) - 1






