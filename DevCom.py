
import pygame

from dataManagers import steamWrapper, TileScan, flipBookHandler

steamAPI = steamWrapper.API(True)
pygame.init()
pygame.display.init()

screen = None

def loadScreen():
    global screen
    screen = pygame.display.set_mode([0, 0])

def showFBImage(flipbook, index=None):
    global screen

    image = flipbook.returnImage(index)
    screen = pygame.display.set_mode(image.get_size())


    screen.blit(image, [0, 0])
    pygame.display.flip()
    raw_input("Press Enter to Continue:")
    screen = pygame.display.set_mode([0, 0])

print "Welcome to Comical's Developer Command Line Interface!"

def viewTile(inTileSet, gridPos):
    global screen

    image = inTileSet.getTile(gridPos)
    screen = pygame.display.set_mode(image.get_size())

    screen.blit(image, [0, 0])
    pygame.display.flip()
    raw_input("Press Enter to Continue:")
    screen = pygame.display.set_mode([0, 0])

while True:
    exec raw_input("--> ")