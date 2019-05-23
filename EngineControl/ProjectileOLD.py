import pygame, math

class InstProjectile(pygame.sprite.Sprite):
    def __init__(self, pos, dimens, angle, speed, multiplier, lifeTime, Friendly, damage, projList):
        self.image = pygame.Surface(dimens)
        self.rect = pygame.Rect(pos, dimens)
        self.shouldKill = False
        self.lifeTime = lifeTime
        self.multiplier = multiplier
        self.lifeSpan = 0
        self.radius = 20
        self.friendly = Friendly
        self.damage = damage
        self.startPos = pos
        self.drawAfter = 0




        self.envProjMaster = projList
        # print angle



        self.momentum = [ speed * math.cos(angle), speed * math.sin(angle)]
    
    def updateMove(self):
        self.rect.move_ip(self.momentum)
        self.lifeSpan += 1

    def onHit(self):
        self.shouldKill = True
        
    
    
    def updateDraw(self):
        self.image.fill([255, 255, 255])


# Pulse Laser:
class InstPulseLaser(InstProjectile):
    def __init__(self, pos, angle, projList):
        
        super(InstPulseLaser, self).__init__([pos[0], pos[1] + 20], [30,30], angle, 20, 3, 150, True, 10,  projList)
        self.image = pygame.image.load("_IMAGES\Sprites\Projectiles\Pulse.png")
        self.drawAfter = 1
    
    def updateDraw(self):
        pass

    def onHit(self):
        self.envProjMaster.append(InstPulseLaserArtifact([self.rect.x, self.rect.y], 0, self.envProjMaster))
        self.shouldKill = True


class PlayerBladeSlash(InstProjectile):
    def __init__(self, pos, angle, projList):
        super(PlayerBladeSlash, self).__init__([pos[0], pos[1]], [64, 64], angle, 5, 1, 1, True, 10, projList)
        self.image = pygame.image.load("_IMAGES\Sprites\Projectiles\PlayerBladeSlash.png")
        self.image = pygame.transform.rotate(self.image, angle)
        self.image = self.image.convert_alpha()
        self.drawAfter = 0

    def updateDraw(self):
        pass

    def onHit(self):
        # self.envProjMaster.append(InstPulseLaserArtifact([self.rect.x, self.rect.y], 0, self.envProjMaster))
        self.shouldKill = True

class InstPulseLaserArtifact(InstProjectile):
    def __init__(self, pos, angle, projList):
        super(InstPulseLaserArtifact, self).__init__([pos[0], pos[1]], [30, 30], angle, 0, 1, 2, True, 0, projList)
        self.imgList = [pygame.image.load("_IMAGES\Sprites\Projectiles\PulseArtifact1.png"), pygame.image.load("_IMAGES\Sprites\Projectiles\PulseArtifact2.png")]
        self.image = self.imgList[0]
        self.drawAfter = 0

    def updateDraw(self):
        if self.lifeSpan > self.lifeTime/2:
            self.image = self.imgList[1]

    def onHit(self):
        pass



# Particle Beam:
class InstParticleBeam(InstProjectile):
    def __init__(self, pos, angle, projList):
        super(InstParticleBeam, self).__init__([pos[0], pos[1] + 20], [30,30], angle, 20, 1, 300, True, 25,  projList)
        self.image = pygame.image.load("_IMAGES\Sprites\Projectiles\Particle.png")
        self.drawAfter = 2
    
    def updateDraw(self):
        pass




class InstEnemyParticleBeam(InstProjectile):
    def __init__(self, pos, angle, projList):
        super(InstEnemyParticleBeam, self).__init__([pos[0], pos[1] + 20], [30, 30], angle, 20, 1, 300, False, 1, projList)
        self.image = pygame.image.load("_IMAGES\Sprites\Projectiles\EnemyParticle.png")
        self.drawAfter = 2

    def updateDraw(self):
        pass