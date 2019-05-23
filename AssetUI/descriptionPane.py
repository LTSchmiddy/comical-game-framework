import pygame

from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler

pygame.init()
pygame.font.init()

class DescriptionPane(object):
    def __init__(self, pos, dimens, offset, size = 40, textColor=[0, 0, 0], fillColor=[255, 235, 135]):
        self.pos = pos
        self.dimens = dimens
        self.screenOffset = offset
        self.rect = pygame.Rect(pos, dimens)
        self.size = size
        self.fillColor = fillColor
        self.textColor = textColor
        self.textStartingPoint = 10


        self.scrollSpeed = 20

        self.textOffset = 10

        self.text = ""
        self.icon = None

        self.image = pygame.Surface(self.dimens)
        self.textArea = pygame.Surface([self.dimens[0], self.dimens[1] - self.textStartingPoint])
        self.textArea.fill(self.fillColor)

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", self.size)

    def eventLoop(self, events):
        # self.text = ""
        # for i in events["mstate"]:
        #     self.text = self.text + str(i) + ", "
        # self.renderText()


        if self.rect.collidepoint( [pygame.mouse.get_pos()[0] - self.screenOffset[0], pygame.mouse.get_pos()[1] - self.screenOffset[1]]):
            self.textStartingPoint += events["mstate"][3] * self.scrollSpeed



    def renderText(self, text = None, useIcon = None):
        if text != None:
            self.text = text

        self.icon = useIcon

        if self.icon == None:
            # self.icon = pygame.Surface([32, 32])
            self.icon = pygame.Surface([1, 1])
            self.icon.fill(self.fillColor)

        self.textStartingPoint = 10

        # self.textArea.fill(self.fillColor)
        textList = self.text.split(" ")

        # Parsing For Word Wrapping:
        newTextStr = ""
        nextLineStr = ""
        nextWord = ""
        while len(textList) > 0:
            nextWord = textList.pop(0)

            if "\n" in nextWord:
                wordSplit = nextWord.split("\n")
                newTextStr = newTextStr + "\n" + nextLineStr + " " + wordSplit[0]
                nextLineStr = wordSplit[1]
            else:

                if self.fontRend.size(nextLineStr + nextWord)[0] > self.dimens[0] - self.textOffset - 20:
                    newTextStr = newTextStr + "\n" + nextLineStr
                    nextLineStr = nextWord
                else:
                    nextLineStr = nextLineStr + " " + nextWord

        newTextStr = newTextStr + "\n" + nextLineStr

        # Rendering:
        drawStart = 10

        newTextList =  newTextStr.split("\n")

        self.textArea = pygame.Surface([self.dimens[0], self.dimens[1] + (self.fontRend.size(newTextList[0])[1] * len(newTextList)) + self.icon.get_height() - self.textStartingPoint])

        self.textArea.fill(self.fillColor)
        self.textArea.blit(self.icon, [self.textOffset, drawStart])
        drawStart = drawStart + self.icon.get_height()

        for i in newTextList:
            if i != "":
                rendered = self.fontRend.render(i, True, self.textColor)
                self.textArea.blit(rendered, [self.textOffset, drawStart])
                drawStart = drawStart + rendered.get_height()



    def Draw(self):
        self.image.fill(self.fillColor)
        self.image.blit(self.textArea, [0, self.textStartingPoint])
        pygame.draw.rect(self.image, [0, 0, 0], pygame.Rect([0, 0], self.dimens), 10)


