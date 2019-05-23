import pygame, gameSettingsMaster, os
from pygame import mixer

# pygame.init()
mixer.init()
# mixer.music.init()

mixer.set_num_channels(gameSettingsMaster.getSettingsDict()["Audio"]["Number of Audio Channels"])

class AudioController:
    def __init__(self):
        import pygame, gameSettingsMaster
        from pygame import mixer

        # Game Music Tracks
        self.songPathDict = {}


        self.soundDict = {
            "AngelFishJingle":pygame.mixer.Sound("_AUDIO\\SONGS\\Jingles\\AFJ.wav")
        }
        self.channelDict = {}

        self.music = pygame.mixer.music

        # self.setMusicTrack(None)


    def reloadSoundEffects(self):
        pass

    def triggerSound(self, label):
        return self.soundDict[label].play()

    def silenceAll(self):
        for i in self.soundDict:
            self.soundDict[i].stop()

    def setMusicTrack(self, trackLabel):
        self.music.load("_AUDIO\\SONGS\\GameMusic\\" + trackLabel + ".wav")
        self.music.play(-1)

    def mainLoop(self):
        pass





#     An audio controller for individual game objects, like the player or enemies:
class SoundController:
    def __init__(self):
        # Sound Effect Objects
        self.soundDict = {}
        self.soundPlaying = {}
        # Channel Objects
        self.channelDict = {}

    def prepSounds(self):
        for i in self.soundDict:
            self.soundPlaying[i] = False

    def triggerSound(self, label, loop = 0):
        # print self.soundDict
        self.soundDict[label].play(loop)

    def silenceAll(self):
        for i in self.soundDict:
            self.soundDict[i].stop()

        for i in self.soundDict:
            self.soundPlaying[i] = False

    def playSound(self, label, loop = 0):
        if self.soundPlaying[label] == False:
            self.soundDict[label].play(loop)
            self.soundPlaying[label] = True

    def stopSound(self, label):
        self.soundDict[label].stop()
        self.soundPlaying[label] = False

    def playOnChannel(self, label, loop = 0):
        if not label in self.channelDict:
            self.channelDict[label] = self.soundDict[label].play(loop)
        else:
            if self.channelDict[label].get_busy() and (self.channelDict[label].get_sound() == self.soundDict[label]):
                pass
            else:
                self.channelDict[label] = self.soundDict[label].play(loop)

    # def dedicateChannel(self, label):
    #     self.channelDict[label] = self.soundDict[label]

    def clearChannel(self, label):
        del self.channelDict[label]

    def loadFromDir(self, dir, vol):
        soundPaths = os.listdir(dir)
        for i in range(0, len(soundPaths)):
            soundPaths[i] = dir + "/" + soundPaths[i]

        self.loadFromPaths(soundPaths)

    def loadFromPaths(self, pathList, vol=1):
        for i in pathList:
            pathSplit = i.split("\\")
            soundID = pathSplit.pop().split(".")[0]
            self.soundDict[soundID] = mixer.Sound(i)
            self.soundDict[soundID].set_volume(vol)
        self.prepSounds()

    def loadFromDir2(self, dir, vol):
        soundPaths = os.listdir(dir)
        for i in range(0, len(soundPaths)):
            soundPaths[i] = dir + "/" + soundPaths[i]

        self.loadFromPaths2(soundPaths)

    def loadFromPaths2(self, pathList, vol=1):
        for i in pathList:
            pathSplit = i.split("/")
            soundID = pathSplit.pop().split(".")[0]
            self.soundDict[soundID] = mixer.Sound(i)
            self.soundDict[soundID].set_volume(vol)
        self.prepSounds()