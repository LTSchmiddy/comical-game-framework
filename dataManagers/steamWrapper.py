import ctypes
import os
import steam


def getLib():
    lib = ctypes.cdll.LoadLibrary(os.getcwd() + "\\SBPv2.dll")
    return lib

def getDevLib(devFolder):
    lib = ctypes.cdll.LoadLibrary(devFolder + "\\SBPv2.dll")
    return lib


class API():
    def __init__(self, isSteamEnabled, useDev = False, devPath = None):
        # Load module. I don't plan on calling it directly, but just in case:
        self.isSteamEnabled = isSteamEnabled
        self.devMode = useDev

        if not self.isSteamEnabled:
            return

        self.module = steam

        # Load features from the module:
        self.client = steam.SteamClient
        self.web = steam.WebAPI
        self.sid = steam.SteamID
        self.gid = steam.GlobalID
        self.auth = steam.WebAuth


        # Load the API DLL
        self.lib = None
        self.devMode = useDev
        if self.devMode:
            if devPath != None:
                self.lib = getDevLib(devPath)
            else:
                self.lib = getLib()
        else:
            self.lib = getLib()

    def initSteam(self):
        if not self.isSteamEnabled:
            if self.devMode:
                print "Steam Integration is not enabled for your game."
            return

        return int(self.lib.initSteam())



    def getSpam(self):
        if not self.isSteamEnabled:
            if self.devMode:
                print "Steam Integration is not enabled for your game."
            return "Steam functionality is disabled in your project."


        return ctypes.c_char_p(self.lib.spam_system()).value
