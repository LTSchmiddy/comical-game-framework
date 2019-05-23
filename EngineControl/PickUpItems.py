import pygame, GameStat, os, runpy, flipAnim
from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler



class InstPickup (pygame.sprite.Sprite):
    def __init__ (self, pos, itemRef, world):
        super(InstPickup, self).__init__()

        self.tag = "Pickup"
        self.world = world
        self.itemRef = itemRef
        # self.itemRef = itemRef
        # self.item = self.itemRef(world)
        self.item = world.items[self.itemRef]
        self.image = None
        self.anim = None
        self.loadImages()

        self.rect = pygame.Rect(pos, [self.image.get_width(), self.image.get_height()])
        self.radius = 128

        self.shouldDie = False

    def loadImages(self):
        self.item = self.world.items[self.itemRef]
        self.image = contentHandler.loadImage(self.item.imagePath)
        if self.item.animated:
            self.anim = flipAnim.Animation(20)
            self.anim.loadFramesFromFolder(self.item.animDir)

    def sanitize(self):
        del self.image
        del self.item


    def runAI(self):
        pass

    def onUse(self):
        self.item.onUse()
        self.shouldDie = True

    def onPickup(self):
        self.world.updateInvUI = True
        self.world.mainPlayer.addItem(self.item.id, 1)
        self.shouldDie = True

    def onInteract(self):
        pass

    def updateDraw(self):
        if self.item.animated:
            self.image = self.anim.getFrame()

class InstCoinPickup(pygame.sprite.Sprite):
    def __init__(self, pos, value, world):
        super(InstCoinPickup, self).__init__()
        self.tag = "Coin"
        self.world = world
        self.value = value
        # self.itemRef = itemRef
        # self.item = self.itemRef(world)
        self.image = None
        # self.anim = None
        self.loadImages()

        self.rect = pygame.Rect(pos, [self.image.get_width(), self.image.get_height()])
        # self.radius = 128

        self.shouldDie = False

    def loadImages(self):
        self.image = pygame.image.load("_IMAGES\\Sprites\\Pickups\\Gold_Coin\\GoldCoin.png")

    def sanitize(self):
        del self.image

    def runAI(self):
        pass

    def onInteract(self):
        self.world.updateInvUI = True
        self.world.mainPlayer.money.modValue(self.value)
        self.shouldDie = True

    def updateDraw(self):
        pass

# Item Class:

class InstItem(object):
    def __init__ (self, world, itemDict = None, fileName = ""):
        self.world = world
        self.fileName = fileName
        self.itemDict = itemDict
        self.equip = None
        self.desc = ""
        self.id = "item"
        self.name = "Game Item"
        self.imagePath = "_IMAGES\\Sprites\\Pickups\\Health\\HealthItem32.png"
        self.value = 0
        self.animated = False
        self.animDir = None

        self.canSell = True

        self.OnUseFunct = None

        self.OnEquipFunct = None
        self.OnRemoveFunct = None
        self.OnCollectFunct = None

        self.consumeOnUse = True

        if self.itemDict != None:
            self.loadFromDict(self.itemDict)

    def loadFromDict(self, dict):
        self.itemDict = dict
        self.id = dict["itemID"]
        self.desc = dict["desc"]
        self.name = dict["name"]
        self.imagePath = dict["imagePath"]
        # self.OnUseFunct = dict["onItemUse"]
        # self.animated = dict["animated"]

        if "equip" in dict:
            self.equip = dict["equip"]

        if self.equip != None:

            self.OnEquipFunct = dict["onItemEquip"]

            self.OnRemoveFunct = dict["onItemRemove"]

            if self.equip == "Weapon":
                self.OnUseFunct = dict["onItemUse"]

        else:
            self.OnUseFunct = dict["onItemUse"]

        if "onItemCollect" in dict:
            self.OnCollectFunct = dict["onItemCollect"]


        if "animDir" in dict:
            self.animated = True
            self.animDir = dict["animDir"]

        if "value" in dict:
            self.value = dict["value"]

        if "consumeOnUse" in dict:
            self.consumeOnUse = dict["consumeOnUse"]

        if "canSell" in dict:
            self.canSell = dict["canSell"]
            # self.canSell = True

    def onCollect(self):
        if self.OnCollectFunct != None:
            self.OnCollectFunct(self.world, self)

    def onUse(self):
        self.OnUseFunct(self.world, self)

    def onEquip(self):
        self.OnEquipFunct(self.world, self)

    def onUnequip(self):
        self.OnRemoveFunct(self.world, self)


class ItemManager:
    def __init__(self, world, itemDir = "EngineControl\\GamePlayObjects\\Items", loadOnInit = True):
        self.itemList = {}
        self.itemDir = itemDir
        self.world = world

        if loadOnInit:
            self.loadItems()

    def __getitem__(self, i):
        return self.itemList[i]

    def doesItemExist(self, itemID):
        for i in self.itemList:
            if itemID == self.itemList[i].id:
                return True

        return False

    def liveLoadItem(self, itemID):
        del self.itemList[itemID]
        self.loadNewItem(itemID + ".item")

    def liveLoadItemFile(self, file):
        itemID = None
        for i in self.itemList:
            if self.itemList[i].fileName == file:
                itemID = i
                break

        del self.itemList[itemID]
        self.loadNewItem(itemID + ".item")

    def reloadItems(self):
        self.itemList = {}
        self.loadItems()

    def loadItems(self):
        for i in os.listdir(self.itemDir):
            self.loadNewItem(i)

    def loadFromContPacks(self):
        for pack in self.world.contentPackageManager.packDict:
            for item in self.world.contentPackageManager.packDict[pack].itemDicts:
                self.loadNewItemFromContPack(item, pack)

    def loadNewItem(self, item):
        filePath = self.itemDir + "\\" + item
        cModDict = runpy.run_path(filePath)
        self.itemList[cModDict["itemID"]] = InstItem(self.world, cModDict, item)

    def loadNewItemFromContPack(self, item, pack):

        cModDict = self.world.contentPackageManager.getPackage(pack).itemDicts[item]
        self.itemList[cModDict["itemID"]] = InstItem(self.world, cModDict, item)

    def listItems(self):
        retVal = {}
        for i in self.itemList:
            retVal.update({i: self.itemList[i].fileName})

        print retVal
        return retVal




