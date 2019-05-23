
class StoreManager:
    def __init__(self):
        self.storeItems = None

    def loadStore(self, items):
        self.storeItems = items

    def getStore(self):
        retVal = self.storeItems
        self.storeItems = None
        return retVal