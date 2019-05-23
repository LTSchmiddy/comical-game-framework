import cherrypy, os, json


serverConf = {
    '/': {
        'tools.sessions.on': True,
        'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': './EditorSystem/static'
    }
}

hostvar = None

def launchServer(hostvarIn):
    global serverConf, hostvar
    mainUIServer = UIServer(hostvarIn)
    cherrypy.server.socket_port = 25397
    cherrypy.quickstart(mainUIServer, "/", serverConf)




def getPage(name):
    pageFile = open(''.join(["/EditorSystem/ServerPages/", name]))
    return pageFile.read()


class UIServer(object):
    def __init__ (self, hostVar):
        self.data = {}
        self.hostVar = hostVar

    @cherrypy.expose
    def index(self, cont = "Items"):

        indexStr = self.getPage("index")
        try:
            pageFile = open(''.join(["EditorSystem\\DisplayContent\\", cont, ".htm"]))
            return pageFile.read().join(indexStr.split("<!-- ContentArea -->"))
        except:
            pageFile = open(''.join(["EditorSystem\\DisplayContent\\", "Oops.htm"]))
            return pageFile.read().join(indexStr.split("<!-- ContentArea -->"))



    def getPage(self, name):
        pageFile = open(''.join(["EditorSystem\\serverPages\\", name, ".html"]))
        return pageFile.read()

    # Data Retrieval:
    @cherrypy.expose
    def getItemList(self):
        return json.dumps(self.hostVar["Game Env"].items.listItems())

    @cherrypy.expose
    def loadItemScript(self, itemFile):
        pageFile = open(''.join(["EngineControl/GamePlayObjects/Items/", itemFile]))
        return pageFile.read()

    @cherrypy.expose
    def saveItemScript(self, itemFile, text):
        pageFile = open(''.join(["EngineControl/GamePlayObjects/Items/", itemFile]), "w")

        pageFile.write(text)
        pageFile.close()
        self.hostVar["Game Env"].items.liveLoadItemFile(itemFile)

        # print text

    @cherrypy.expose
    def createNewItem(self, newItemName):
        pageFile = open(''.join(["EngineControl/GamePlayObjects/Items/", newItemName, ".item"]), "w")

        newText = """
itemID = "***NewItem***"
desc = "New Item Description"
name = "New Item"
value = 30
equip = None

consumeOnUse = True

imagePath = "_IMAGES\\Sprites\\Items\\Telepathy Book\\TelepathyBook.png"


def onItemUse(world, item=None):
    pass

def onItemEquip(world, item=None):
    pass


def onItemRemove(world, item=None):
    pass     
        
        """

        newTextNamed = newItemName.join(newText.split("***NewItem***"))


        pageFile.write(newTextNamed)
        pageFile.close()
        self.hostVar["Game Env"].items.loadNewItem(newItemName + ".item")

    @cherrypy.expose
    def giveToPlayer(self, item):
        self.hostVar["Game Env"].mainPlayer.addItem(item)







