import pygame, EnviroObject, flipAnim


class InteractionMarker(pygame.sprite.Sprite):
    def __init__(self, world):
        super(InteractionMarker, self).__init__()
        self.rect = pygame.Rect([0, 0], [64, 64])
        self.image = pygame.Surface([64, 64])

        self.fontRend = pygame.font.Font("_IMAGES\\ComicSans.ttf", 25)
        self.text = ""

        self.show = True

    def setText(self, text, inAlpha = 200, useColor = [255, 235, 135]):
        self.text = text
        newMsg = self.fontRend.render(text, True, [0, 0, 0])
        self.image = pygame.Surface([newMsg.get_width() + 40, newMsg.get_height() + 40])
        self.image.fill(useColor)
        pygame.draw.rect(self.image, [0, 0, 0], pygame.Rect([0, 0], self.image.get_size()), 10)
        self.image.blit(newMsg, [20, 20])

        self.rect.size = self.image.get_size()

        self.image.set_alpha(inAlpha)


    def setPos(self, pos):
        self.rect.bottomleft = [pos[0], pos[1] - 30]


    def Draw(self):
        pass







class InteractiveTile (pygame.sprite.Sprite):
    def __init__ (self, pos, dimens, player, persist):
        super(InteractiveTile, self).__init__()
        self.image = pygame.Surface(dimens)
        self.rect = pygame.Rect(pos, dimens)
        self.image.fill([255, 255, 255])
        self.mainPlayer = player
        self.persist = persist

    def runAI(self, persist):
        pass

    def onHit(self):
        pass

    def updateDraw(self):
        pass


class EnvLocalTransitionTile (InteractiveTile):
    def __init__ (self, pos, destination, player, persist):
        super(EnvLocalTransitionTile, self).__init__(pos, [64, 64], player, persist)

        self.destination = destination
        self.isHit = False
        self.loadImages()



    def runAI(self, persist):
        pass

    def onHit(self):
        self.isHit = True

    def updateDraw(self):
        self.image = self.anim.getFrame()

    def loadImages(self):
        self.anim = flipAnim.Animation(20)
        self.anim.loadFramesFromFolder("C:\Users\Alex Schmid\Google Drive\Code\Python\Comical\_IMAGES\Sprites\Transition Pads\\" + self.destination, ".png")
        self.image = self.anim.getFrame()

    def sanitize(self):
        del self.anim
        del self.image



# class InteractionModule:
#     def __init__(self, ID):
