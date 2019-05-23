import pygame, math

class Stat(object):
    def __init__(self, startVal, min, max, inRegenSpeed = 0, inRegenDelay = 0, inDesc="", buffable=True):
        self.value = startVal

        self.min = min
        self.max = max
        
        self.regenSpeed = inRegenSpeed
        self.regenDelay = inRegenDelay
        # self.regenSpeedCounter = 0
        self.regenDelayCounter = 0
        
        self.description = inDesc

        self.buff = None
        self.buffMax = None
        self.buffMin = None
        self.buffDelay = None
        self.buffSpeed = None
        

        self.weak = None
        self.weakMax = None
        self.weakMin = None
        self.weakDelay = None
        self.weakSpeed = None


        if buffable:
            self.setClearModifiers()

    def setClearModifiers(self):
            self.buff = Stat(0, 0, float("inf"), 0, 0, "", False)
            self.buffMax = Stat(0, 0, float("inf"), 0, 0, "", False)
            self.buffMin = Stat(0, 0, float("inf"), 0, 0, "", False)
            self.buffDelay = Stat(0, 0, float("inf"), 0, 0, "", False)
            self.buffSpeed = Stat(0, 0, float("inf"), 0, 0, "", False)

            
            self.weak = Stat(0, 0, float("inf"), 0, 0, "", False)
            self.weakMax = Stat(0, 0, float("inf"), 0, 0, "", False)
            self.weakMin = Stat(0, 0, float("inf"), 0, 0, "", False)
            self.weakDelay = Stat(0, 0, float("inf"), 0, 0, "", False)
            self.weakSpeed = Stat(0, 0, float("inf"), 0, 0, "", False)



    def __str__(self):
        return str(self.getValue()) + " on a scale of " + str(self.getMin(False)) + " to " + str(self.getMax(False))

    def getOutOfStr(self):
        return str(self.getValue()) + " out of " + str(self.getMax(False))

    def getDashStr(self):
        return str(self.getValue()) + "/" + str(self.getMax(False))
    
    def regenTick(self):
        if self.buff != None:
            if self.regenDelay - self.buffDelay.getValue() > self.regenDelayCounter:
                self.regenDelayCounter += 1
            else:
                self.value += self.regenSpeed + self.buffSpeed.getValue()



        else:
            if self.regenDelay > self.regenDelayCounter:
                self.regenDelayCounter += 1
            else:
                self.value += self.regenSpeed
        self.trim()
            
    
    # Current Value
    def setValue(self, inVal):
        self.regenDelayCounter = 0
        self.value = inVal
        self.trim()
        
    def getValue(self, needTrim=True):
        if needTrim:
            self.trim()

        if self.buff != None:

            retVal = self.value - self.weak.getValue()
            if retVal < self.getMin(False):
                retVal = self.getMin(False)

            retVal += self.buff.getValue()

            if retVal > self.getMax(False):
                retVal = self.getMax(False)

            return retVal
        else:
            return self.value

    def getCleanValue(self, needTrim=True):
        if needTrim:
            self.trim()

        return self.value
        
    def modValue(self, modVal):
        self.regenDelayCounter = 0
        self.value += modVal
        self.trim()
    
    def hasEnough(self, amount):
        self.trim()
        if self.getValue() - self.getMin() >= amount:
            return True
        else:
            return False

    def tryToUse(self, amount):
        if self.hasEnough(amount):
            self.modValue(-amount)
            return True
        else:
            return False
    
    # Maximum
    def setMax(self, inVal):
        self.max = inVal
        self.trim()


    def getMax(self, needTrim=True):
        if needTrim:
            self.trim()

        if self.buff != None:
            return self.max - self.weakMax.getValue() + self.buffMax.getValue()
        else:
            return self.max


    def getIsFull(self, needTrim=True):
        if needTrim:
            self.trim()
        if self.getValue(False) >= self.getMax(True):
            return True
        return False

    def getCleanMax(self, needTrim=True):
        if needTrim:
            self.trim()
        return self.max
    
    def modMax(self, modVal):
        self.max += modVal
        self.trim()
    
    # Minimum
    def setMin(self, inVal):
        self.min = inVal
        self.trim()
        
    def getMin(self, needTrim=True):
        if needTrim:
            self.trim()
        if self.buff != None:
            return self.min - self.weakMin.getValue() + self.buffMin.getValue()
        else:
            return self.min


    def getCleanMin(self, needTrim=True):
        if needTrim:
            self.trim()
        return self.min
    
    def modMin(self, modVal):
        self.min += modVal
        self.trim()
    
    
    # **************
    def trim(self):
        if self.buff != None:
            if self.value > self.getMax(False):
                self.value = self.getMax(False)

            if self.value < self.getMin(False):
                self.value = self.getMin(False)
        else:
            if self.value > self.max:
                self.value = self.max

            if self.value < self.min:
                self.value = self.min



def getDist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])