




class metaArchive:
    def __init__(self, world):
        self.world = world

        self.worldEnvData = {}
        # if len (self.worldEnvData) == 0:
        #     self.loadDefaults()

        self.charMemory = {
            "Madikae": {
                "Has Met Player": False
            }
        }


    def hasLvlKey(self, key):
        if not (key in self.worldEnvData):
            self.worldEnvData[key] = {}

    def setEnvValue(self, objLabel, key, value):
        self.setRemoteValue(self.world.currentGrid, self.world.worldGridPos, objLabel, key, value)


    def getEnvValue(self, objLabel, key, default = None):
        return self.getRemoteValue(self.world.currentGrid, self.world.worldGridPos, objLabel, key, default)


    def getRemoteValue(self, grid, gridPos, objLabel, key, default):
        if not (grid in self.worldEnvData):
            self.worldEnvData[grid] = {}

        gpStr = str(gridPos)

        if not (gpStr in self.worldEnvData[grid]):
            self.worldEnvData[grid][gpStr] = {}

        if not (objLabel in self.worldEnvData[grid][gpStr]):
            self.worldEnvData[grid][gpStr][objLabel] = {}

        if not (key in self.worldEnvData[grid][gpStr][objLabel]):
            self.worldEnvData[grid][gpStr][objLabel][key] = default

        return self.worldEnvData[grid][gpStr][objLabel][key]

    def setRemoteValue(self, grid, gridPos, objLabel, key, value):
        if not (grid in self.worldEnvData):
            self.worldEnvData[grid] = {}

        gpStr = str(gridPos)
        if not (gpStr in self.worldEnvData[grid]):
            self.worldEnvData[grid][gpStr] = {}

        if not (objLabel in self.worldEnvData[grid][gpStr]):
            self.worldEnvData[grid][gpStr][objLabel] = {}

        self.worldEnvData[grid][gpStr][objLabel][key] = value
        
        
    #
    # def loadDefaults(self):
    #     self.worldEnvData = {
    #         "_OverWorld": {
    #             "[100, 100]": {
    #                 "Lever1": {
    #                     "state": True
    #                 }
    #             }
    #         }
    #
    #     }


