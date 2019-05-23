import pygame, pickle, time

pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode([256, 256])
# testSound = pygame.mixer.Sound("testSoundFile.wav")
#
# ch = testSound.play()
# print "Playing!!"
#
#
#
# print "Making Array:"
# testArray = pygame.sndarray.array(testSound)
# fileWrite = open("test.sar", "w")
#
# pickle.dump(testArray, fileWrite)


fileRead = open("test.sar", "r")
array = pickle.load(fileRead)
loadSound = pygame.sndarray.make_sound(array)

loadSound.play()


time.sleep(2)
exit()