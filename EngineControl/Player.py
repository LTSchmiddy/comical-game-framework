import GameStat
import Projectile
import gameSettingsMaster
import math
import os
import pygame
import LevellingSystem
import random
import copy
from dataManagers import audioMan, counter
from dataManagers import contentPackages
contentHandler = contentPackages.mainHandler


class InstPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, world):
        super(InstPlayer, self).__init__()

        self.world = world
        self.pos = pos
        self.dimens = [25, 70]

        self.noClip = False
        
        
        self.offsetBody = [0, 0]

        self.typeMode = "Player"

        self.loadImages()
        # Legs Draw MetaData
        self.LRFrame = 0
        self.LRFCounter = 0
        self.LRFCMax = 5

        self.showHitCounter = counter.TickCounter(30, False, True)
        self.showHitCounter.setTime(15)


        self.offsetLegs = [0, 0]
        self.offsetLegsRight = [-15, 45]
        self.offsetLegsLeft = [-10, 45]
        self.offsetLegsBack = [-13, 45]
        self.offsetLegsForward = [-12, 45]
        
        self.offsetLegs[0] = self.offsetLegsRight[0]
        self.offsetLegs[1] = self.offsetLegsRight[1]

        
        #Arms Draw MetaData

        self.offsetTopArmRight = [2, 28]
        self.offsetBottomArmRight = [10, 28]
        self.offsetTopArmLeft = [-8, 28]
        self.offsetBottomArmLeft = [-16, 28]

        self.TopArmNoAimLeftOffSet = [-47, 28]
        self.BottomArmNoAimRightOffSet = [-43, 28]


        self.SwordArmLeftOffset = [-45, 28]
        self.SwordArmRightOffset = [-53, 28]

        self.WeaponsForwardOffset = [-50, 33]
        self.AttackSwordbackOffset = [-50, -8]

        self.offsetTopArm = [2, 8]
        self.offsetBottomArm = [8, 28]

        self.offsetBox = [0, 0]
        self.rect = pygame.Rect(self.pos, self.dimens)
        self.radius = 100




        # Projectile Data:
        
        #Beam MetaData
        self.fireAngle = 0
        self.fireBeam = 0
        self.endBeam = [0, 0]


        # Some of this is old and not used, but I'm not sure what... yet. Remove Later
        self.projectileList = [Projectile.InstProjectileDesc]
        self.projectileCost = [20, 2]
        self.projectileRates = [10, 5]
        self.projectileWeapName = ["Pulse Laser", "Particle Beam"]
        self.projectileIndex = 0
        self.lastFired = 0
        #Player Control MetaData
        self.faceDir = "r"


        self.aiming = False

        self.SwordAttack = False

        self.useMagicArm = False


        self.inFluid = False
        self.allowDown = True
        self.allowLeft = True
        self.allowRight = True
        self.allowUp = True
        
        self.momentum = [0, 0]
        self.extraMomentum = [0, 0]

        self.inputTracker = { "w":False, "s":False, "a":False, "d":False, "space":False, "FatalBlitz":False}
        
        # Player Stats MetaData
        self.stats = {
            "health":GameStat.Stat(100, 0, 100),
            "weapEnergy": GameStat.Stat(100, 0, 100, .5, 60),
            "magic": GameStat.Stat(100, 0, 100),
            "attrSpeed":GameStat.Stat(7, 0, 100),
            "attrAimSpeed": GameStat.Stat(7, 0, 100),
            "attrJump": GameStat.Stat(13, 0, 100),
            "attrDam": GameStat.Stat(1, 0, 100),
            "pwrBlitz": GameStat.Stat(0, 0, 5, 0, 0, "", False),
            "pwrBurn": GameStat.Stat(0, 0, 5, 0, 0, "", False)
        }

        self.blitzCost = 5
        self.usingBurn = False

        self.burnCost = 75

        self.money = GameStat.Stat(0, 0, 1000)
        self.XP = GameStat.Stat(0, 0, float("inf"), 0, 0, "", False)
        self.inventory = {
            "HealthItem": GameStat.Stat(5, 0, 20),
            "SMG1": GameStat.Stat(1, 0, 20),
            "Shotgun1": GameStat.Stat(1, 0, 20)
            # "SpellDemonCore": GameStat.Stat(1, 0, 20),
        }
        self.equipment = {}


        # Weapon Data:
        self.ammo = {
            "nsAmmo":GameStat.Stat(6, 0, 6),
            # "nsAmmo":GameStat.Stat(24, 0, 24),
            "SMG": GameStat.Stat(255, 0, 255),
            "Shotgun": GameStat.Stat(50, 0, 50)
        }
        self.nsAmmoChargeCounter = counter.TickCounter(30, True, False)
        self.currentAmmo = "nsAmmo"
        self.projectileName = "Basic Shot"

        self.bladeProjectile = "Blade Slash"
        # self.bladeProjectile = "BurningHelix"




        self.hotkeyItems = {
            "1": None,
            "2": "HealthItem",
            "3": None,
            "4": None,
            "5": None,
            "6": "SpellDemonCore"
        }

        self.useOnHit = False


        self.level = LevellingSystem.LevelHandler(self)
        self.attrUpgradePoints = GameStat.Stat(0, 0, float("inf"), 0, 0, "", False)
        self.fpwrUpgradePoints = GameStat.Stat(0, 0, float("inf"), 0, 0, "", False)

        self.ctrls = gameSettingsMaster.getSettingsDict()["Controls"]

        self.audio = None
        self.isWalkingSound = False
        self.loadAudio()

        self.respawnPoint = ["_Overworld", [100, 100]]


    
    def bgTasks(self):
        self.showHitCounter.check()

        if self.extraMomentum[0] > 0:
            self.extraMomentum[0] -= 1
        if self.extraMomentum[0] < 0:
            self.extraMomentum[0] += 1

        if self.extraMomentum[1] > 0:
            self.extraMomentum[1] -= 1
        if self.extraMomentum[1] < 0:
            self.extraMomentum[1] += 1


        # print self.stats["health"].getValue()
        # for i in self.inventory:
        #     print i
        self.inFluid = False
        self.allowDown = True
        self.allowLeft = True
        self.allowRight = True
        self.allowUp = True
        
        for key in self.stats:
            self.stats[key].regenTick()

        if self.nsAmmoChargeCounter.check():
            self.ammo["nsAmmo"].modValue(1)

        if self.level.checkIfLeveledUp():
            self.world.notif.notify("You Have Reached Level " + str(self.level.getLevel()))
            self.attrUpgradePoints.modValue(1)
            self.fpwrUpgradePoints.modValue(1)
            self.stats["weapEnergy"].modMax(100)
            self.stats["weapEnergy"].modValue(100)
            self.stats["weapEnergy"].regenSpeed += .25
            self.stats["health"].modMax(20)
            self.stats["health"].modValue(20)

    def pushPlayer(self, impact):
        self.extraMomentum[0] += impact[0]
        self.extraMomentum[1] += impact[1]

        # print "IMPACT:", impact


    def setPlayerPos(self, pos, local = False):
        if local:
            pos[0] += self.pos[0]
            pos[1] += self.pos[1]

        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def takeHit(self, damage):
        self.stats["health"].modValue(damage)
        self.showHitCounter.reset()

        for i in range(0, -damage):
            self.world.fireProjectile([self.rect.center[0] - 16, self.rect.top - 36], math.atan2(-1, 0), 20, "PlayerBloodParticle")

    def onDeath(self):
        if self.world.editor != None:
            if self.world.editor.inEditorMode:
                return

        self.extraMomentum = [0, 0]
        self.audio.silenceAll()
        self.audio.triggerSound("OnDeath")
        self.world.flipbook.trigger("OnDeathLongC", 10)
        self.world.triggerEnv([-64, 256], self.respawnPoint[0], self.respawnPoint[1])
        self.stats["health"].setValue(10)
    
    def handleEnvCollision(self, Rect):
        if self.noClip:
            return

        if Rect.direction == "left":
            self.allowRight = False
            if self.rect.right > Rect.left:
                if self.usingBurn:
                    self.momentum[0] += Rect.left - self.rect.width + 5
                else:
                    self.pos[0] = Rect.left - self.rect.width + 5
            
            # print "Left Hit \n ****"
        elif Rect.direction == "right":
            self.allowLeft = False
            if self.rect.left > Rect.right:
                if self.usingBurn:
                    self.momentum[0] += Rect.right + 5
                else:
                    self.pos[0] = Rect.right + 5
            # print "Left Hit \n ****"

        elif Rect.direction == "up":
            self.allowDown = False
            if (self.rect.bottom > Rect.top) and (self.momentum[1] >= 0):
                # self.momentum[1] += Rect.top - self.rect.height + 1
                self.pos[1] = Rect.top - self.rect.height + 1
            
            
        elif Rect.direction == "down":
            self.allowUp = False
            if self.rect.top > Rect.bottom:
                # self.momentum[1] += Rect.bottom + 5
                self.pos[1] = Rect.bottom + 5

    def updateMove(self):

        
        # For platformers. Use to simulate gravity:
        if self.momentum[1] <= 20:
            self.momentum[1] += .5

        # Don't move through solid walls
        if self.allowDown == False:
            if self.momentum[1] > 0:
                self.momentum[1] = 0

            if self.extraMomentum[1] > 0:
                self.extraMomentum[1] = 0

        if self.allowRight == False:
            if self.momentum[0] > 0:
                self.momentum[0] = 0

            if self.extraMomentum[0] > 0:
                self.extraMomentum[0] = 0

        if self.allowLeft == False:
            if self.momentum[0] < 0:
                self.momentum[0] = 0

            if self.extraMomentum[0] < 0:
                self.extraMomentum[0] = 0

        if self.allowUp == False:
            if self.momentum[1] < 0:
                self.momentum[1] = 0

            if self.extraMomentum[1] < 0:
                self.extraMomentum[1] = 0



        if self.inputTracker["FatalBlitz"] and (self.momentum[0] != 0 or (self.momentum[0] == 0 and self.momentum[1] < 0)):
            if self.stats["weapEnergy"].tryToUse(self.blitzCost):
                self.usingBurn = True
                self.spawnProjectile(0, [-64 + self.rect.width/2, -64 + self.rect.height/2], "Blitz")
                self.pos[0] += (self.momentum[0] * 2.5)
                if self.stats["pwrBlitz"].getValue() >= 3 and self.inputTracker["w"]:
                    self.momentum[1] = 0
            else:
                self.usingBurn = False

        else:
            self.usingBurn = False
            self.pos[0] += self.momentum[0]

        self.pos[1] += self.momentum[1]

        self.pos[0] += self.extraMomentum[0]
        self.pos[1] += self.extraMomentum[1]

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
    
    def runEvents(self, events, PlayerOCL, mouseWorld, fireAngle):
        self.fireAngle = fireAngle
        # if len(events["kdown"]) != 0:
        #     print events["kdown"]
        # print pygame.mouse.get_pos()
        #**************
        if self.ctrls["Up"] in events["kdown"] or self.ctrls["Up"] in events["kheld"]:
            self.inputTracker["w"] = True
        else:
            self.inputTracker["w"] = False

        if self.ctrls["Down"] in events["kdown"] or self.ctrls["Down"] in events["kheld"]:
            self.inputTracker["s"] = True
        else:
            self.inputTracker["s"] = False

        if self.ctrls["Left"] in events["kdown"] or self.ctrls["Left"] in events["kheld"]:
            self.inputTracker["a"] = True
        else:
            self.inputTracker["a"] = False

        if self.ctrls["Right"] in events["kdown"] or self.ctrls["Right"] in events["kheld"]:
            self.inputTracker["d"] = True
        else:
            self.inputTracker["d"] = False

        if self.ctrls["Jump"] in events["kdown"] or self.ctrls["Jump"] in events["kheld"]:
            self.inputTracker["space"] = True
        else:
            self.inputTracker["space"] = False

        if (self.ctrls["Use Fatal Blitz"] in events["kdown"] or self.ctrls["Use Fatal Blitz"] in events["kheld"]) and self.stats["pwrBlitz"].getValue() > 0:
            self.inputTracker["FatalBlitz"] = True
        else:
            self.inputTracker["FatalBlitz"] = False

        self.aiming = events["mstate"][2]

        # if self.ctrls["Interact"] in events["kdown"]:
        #     for i in self.world.envInterObj:
        #         if pygame.sprite.collide_circle(self, i):
        #             if i.tag == "Pickup":
        #                 if self.useOnHit:
        #                     i.onPickup()
        #                 else:
        #                     i.onUse()
        #                 break
        useInt = None
        InteractionInRange = False
        for i in self.world.envObj:
            if i.InterMod != None and pygame.sprite.collide_circle(self, i):
                InteractionInRange = True
                useInt = i.InterMod
                if self.world.interactionMarker.text != i.InterMod.onScreenDesc:
                    self.world.interactionMarker.setText(i.InterMod.onScreenDesc)
                self.world.interactionMarker.setPos(i.rect.topleft)
                self.world.interactionMarker.show = True

        if self.ctrls["Interact"] in events["kdown"] and useInt != None:
            useInt.onInteract()

        self.world.interactionMarker.show = InteractionInRange

        #**************
        if 49 in events["kdown"]:
            self.projectileIndex = 0
        if 50 in events["kdown"]:
            self.projectileIndex = 1
        

        # if self.inputTracker["space"] == True and self.allowDown == False:
        #     self.momentum[1] = -15
        if self.aiming:
            if self.world.mouseWorld[0] > self.pos[0] + self.dimens[0]/2:
                self.faceDir = "r"
            else:
                self.faceDir = "l"



            self.SwordAttack = False


            if self.inputTracker["a"] == True:
                self.momentum[0] = -self.stats["attrAimSpeed"].getValue()

            if self.inputTracker["d"] == True:
                self.momentum[0] = self.stats["attrAimSpeed"].getValue()


            # if self.inputTracker["w"] == True:
            #     self.momentum[1] = -self.stats["attrAimSpeed"].getValue()
            #
            # if self.inputTracker["s"] == True:
            #     self.momentum[1] = self.stats["attrAimSpeed"].getValue()

        else:

            self.SwordAttack = events["mstate"][0]




            # if self.inputTracker["w"] == True:
            #     self.momentum[1] = -self.stats["attrSpeed"].getValue()
                # if self.inputTracker["d"] == self.inputTracker["a"]:
                #     self.faceDir = "b"
            #
            # if self.inputTracker["s"] == True:
            #     self.momentum[1] = self.stats["attrSpeed"].getValue()
            #     # if self.inputTracker["d"] == self.inputTracker["a"]:
            #     #     self.faceDir = "f"

            if self.inputTracker["a"] == True:
                self.momentum[0] = -self.stats["attrSpeed"].getValue()
                if not self.ctrls["Strafe"] in events["kheld"]:
                    self.faceDir = "l"

            if self.inputTracker["d"] == True:
                self.momentum[0] = self.stats["attrSpeed"].getValue()
                if not self.ctrls["Strafe"] in events["kheld"]:
                    self.faceDir = "r"


        if self.inputTracker["d"] == self.inputTracker["a"]:
            self.momentum[0] = 0



        # if self.inputTracker["w"] == self.inputTracker["s"]:
        #     self.momentum[1] = 0

        if self.momentum[0] != 0 or self.momentum[1] != 0:

            if self.faceDir == "r":
                if self.momentum[0] > 0:
                    self.countFrame(5)
                else:
                    self.countFrame(-5)
            elif self.faceDir == "l":
                if self.momentum[0] < 0:
                    self.countFrame(5)
                else:
                    self.countFrame(-5)
            elif self.faceDir == "b":
                if self.momentum[1] > 0:
                    self.countFrame(-5)
                else:
                    self.countFrame(5)
            elif self.faceDir == "f":
                if self.momentum[1] < 0:
                    self.countFrame(5)
                else:
                    self.countFrame(-5)





        # print self.momentum
        self.jumpHandler(events)

        for i in range(1, 6):
            if self.ctrls["Hotkey " + str(i)] in events["kdown"]:
                if self.hotkeyItems[str(i)] != None:
                    self.useItem(self.hotkeyItems[str(i)])

                    if self.inventory[self.hotkeyItems[str(i)]].getValue() <= 0:
                        self.hotkeyItems[str(i)] = None

        if 2 in events["mdown"]:
            if self.hotkeyItems["6"] != None:
                self.useItem(self.hotkeyItems["6"])

                if self.inventory[self.hotkeyItems["6"]].getValue() <= 0:
                    self.hotkeyItems["6"] = None

        self.updateMove()
        self.handleFiring(events)
        if 1 in events["mdown"] and not self.aiming:
            # dirAng = 0

            if self.inputTracker["w"]:
                # self.world.envProj.append(Projectile.InstProjectileDesc([self.pos[0] - 20, self.pos[1] + 40], [0, 1], "Blade Slash", self.world))
                self.world.fireProjectile([self.pos[0] - 20, self.pos[1] - 40], math.radians(-90), 0, self.bladeProjectile)

            elif self.inputTracker["s"]:
                # self.world.envProj.append(Projectile.InstProjectileDesc([self.pos[0] - 20, self.pos[1] - 40], [0, -1], "Blade Slash", self.world))
                self.world.fireProjectile([self.pos[0] - 20, self.pos[1] + 40], math.radians(90), 0, self.bladeProjectile)

            elif self.faceDir == "r":
                # self.world.envProj.append(Projectile.InstProjectileDesc([self.pos[0] + 20, self.pos[1]], [1, 0], "Blade Slash", self.world))
                self.world.fireProjectile([self.pos[0] + 20, self.pos[1]], math.radians(0), 0, self.bladeProjectile)
            elif self.faceDir == "l":
                # self.world.envProj.append(Projectile.InstProjectileDesc([self.pos[0] - 60, self.pos[1]], [-1, 0], "Blade Slash", self.world))
                self.world.fireProjectile([self.pos[0] - 60, self.pos[1]], math.radians(180), 0, self.bladeProjectile)


        if self.ctrls["Use Rapid Burn"] in events["kdown"] and not self.aiming and self.stats["pwrBurn"].getValue() >= 1:
            if self.stats["weapEnergy"].tryToUse(self.burnCost):
                if self.faceDir == "r":
                    self.world.envProj.append(Projectile.InstProjectileDesc([self.pos[0] + 20, self.pos[1] - 68], [1, 0], "RapidBurn", self.world))

                elif self.faceDir == "l":
                    self.world.envProj.append(Projectile.InstProjectileDesc([self.pos[0] - 60, self.pos[1] - 68], [-1, 0], "RapidBurn", self.world))





        self.handleAudio()



        if self.stats["health"].getValue() == 0:
            self.onDeath()


    def jumpHandler(self, events):
        if self.ctrls["Jump"] in events["kdown"] and ((self.inFluid) or (not self.allowDown) or (self.stats["pwrBlitz"].getValue() >= 4 and self.ctrls["Use Fatal Blitz"] in events["kheld"] and not self.allowLeft) or (self.stats["pwrBlitz"].getValue() >= 4 and self.ctrls["Use Fatal Blitz"] in events["kheld"] and not self.allowRight)):
            if self.inputTracker["FatalBlitz"] and self.stats["pwrBlitz"].getValue() >= 2:
                self.momentum[1] = -self.stats["attrJump"].getValue() * 2
            else:
                self.momentum[1] = -self.stats["attrJump"].getValue()
            self.audio.triggerSound("Jump")
        if (self.ctrls["Jump"] in events["kup"] or self.ctrls["Use Fatal Blitz"] in events["kup"] or (self.ctrls["Use Fatal Blitz"] in events["kheld"] and self.ctrls["Jump"] in events["kheld"] and self.stats["weapEnergy"].getValue() < self.blitzCost)) and self.allowDown and self.momentum[1] < -5:
            self.momentum[1] = -5

    def handleAudio(self):

        if self.momentum[0] == 0 or self.allowDown == True:
            # self.walkSoundCounter.reset()
            self.audio.stopSound("FootStepPlayerLoop")
            self.isWalkingSound = False


        if self.momentum[0] != 0 and self.momentum[1] == 0:
            self.audio.playSound("FootStepPlayerLoop", -1)
            self.isWalkingSound = True
            # print "Sound"


    def fireBlaster(self):
        self.useMagicArm = False

        if self.ammo[self.currentAmmo].tryToUse(self.world.projectiles.projDict[self.projectileName]["energyUse"]):
        # if self.ammo["nsAmmo"].tryToUse(self.world.projectiles.projDict[self.projectileName]["energyUse"]):

            if not "Weapon" in self.equipment:
                self.spawnProjectile()
                self.nsAmmoChargeCounter.reset()
            else:
                self.world.items[self.equipment["Weapon"]].onUse()

    def spawnProjectile(self, acc = 0, offset = [0, 20], useProj = None):
        angleAdj = 0
        if acc != 0:
            angleAdj = math.radians(random.randint(-acc, acc))
        
        if useProj == None:
            self.world.envProj.append(Projectile.InstProjectileDesc([self.pos[0] + offset[0], self.pos[1] + offset[1]], self.fireAngle + angleAdj, self.projectileName, self.world))
        else:
            self.world.envProj.append(Projectile.InstProjectileDesc([self.pos[0] + offset[0], self.pos[1] + offset[1]], self.fireAngle + angleAdj, useProj, self.world))


    def handleFiring(self, events):

        if self.lastFired > self.world.projectiles.projDict[self.projectileName]["cooldown"]:
            if self.aiming and events["mstate"][0]:
                self.fireBeam = False
                self.fireBlaster()
                # self.world.debugLog.log("FIRE!!")
                self.lastFired = 0
        else:
            self.fireBeam = False
            self.lastFired += 1

    def resetWeapon(self):
        self.projectileName = "Basic Shot"
        self.currentAmmo = "nsAmmo"

    def resetSword(self):
        self.bladeProjectile = "Blade Slash"

    def countFrame(self, direction):

        if direction > 0:
            if self.LRFCounter >= self.LRFCMax:

                if self.LRFrame >= 5:

                    self.LRFrame = 0
                else:
                    self.LRFrame += 1
                self.LRFCounter = 0
            else:
                self.LRFCounter += 1
        else:
            if self.LRFCounter <= 0:

                if self.LRFrame <= 0:

                    self.LRFrame = 5
                else:
                    self.LRFrame -= 1
                self.LRFCounter = self.LRFCMax
            else:
                self.LRFCounter -= 1


    def say(self, text, time=120, offset=[0,0], size=16):
        self.world.wordbubbles.add(text, "player", self.rect, offset, size, time)

    def removeItem(self, itemID, count=1):
        if itemID in self.inventory:
            if self.inventory[itemID].tryToUse(count):
                return True
        return False

    def addItem(self, itemID, count = 1):
        if not self.world.items.doesItemExist(itemID):
            return

        self.world.updateInvUI = True
        if not itemID in self.world.mainPlayer.inventory:
            # self.world.notif.notify("New Item Found: " + self.world.items[itemID].name)
            self.world.mainPlayer.inventory[itemID] = GameStat.Stat(0, 0, 20)
        self.world.mainPlayer.inventory[itemID].modValue(count)
        self.world.items[itemID].onCollect()

    def useItem(self, itemID):
        selectedItem = self.world.items[itemID]
        if itemID in self.inventory:
            if selectedItem.consumeOnUse:
                if self.inventory[itemID].tryToUse(1):
                    self.world.items[itemID].onUse()
                    # self.say("Using a " + selectedItem.name + "!", 120)
                    # self.world.notif.notify("Used a " + selectedItem.name, 120)

                else:
                    self.world.notif.notify("Out of " + selectedItem.name + "s", 120)

            else:
                self.world.items[itemID].onUse()
                # self.say("Using " + selectedItem.name + "!", 120)
                # self.world.notif.notify("Used your " + selectedItem.name, 120)

        else:
            self.world.notify("Missing " + selectedItem.name, 120)

    def equipItem(self, itemID):
        thisItem = self.world.items[itemID]

        if thisItem.equip in self.equipment:
            self.unequipItem(thisItem.equip)

        if self.inventory[thisItem.id].tryToUse(1):
            self.equipment[thisItem.equip] = thisItem.id
            thisItem.onEquip()
            self.say("Equiped " + thisItem.name)
        else:
            self.say("Could Not Equip " + thisItem.name)

    def unequipItem(self, slot):
        if slot in self.equipment:
            thisItem = self.world.items[self.equipment[slot]]
            thisItem.onUnequip()
            self.inventory[thisItem.id].modValue(1)
            del self.equipment[slot]

    def sanitizeInventory(self):
        icop = copy.deepcopy(self.inventory)
        for i in icop:
            if not self.world.items.doesItemExist(i):
                print i, "no longer exists. Removing from Inventory."
                del self.inventory[i]

        ecop = copy.deepcopy(self.equipment)
        for i in ecop:
            if not self.world.items.doesItemExist(self.equipment[i]):
                print self.equipment[i], "no longer exists. Removing from Equipment."
                del self.equipment[i]



    def updateDraw(self, screenX, screenY):

        if self.faceDir == "r":

            if self.showHitCounter.getState():
                self.imgBody = self.imgDict["DamFace Right"]
            elif self.SwordAttack:
                self.imgBody = self.imgDict["AttackFace Right"]
            elif self.aiming:
                self.imgBody = self.imgDict["AimingFace Right"]
            else:
                self.imgBody = self.imgDict["bodyRight"]


            self.offsetLegs[0] = self.offsetLegsRight[0]
            self.offsetLegs[1] = self.offsetLegsRight[1]

            if self.momentum[0] == 0 and self.momentum[1] == 0:

                self.imgLegs = self.imgDict["LS Right"]


            else:
                if self.allowDown:
                    self.imgLegs = self.LRFListRight[0]
                else:
                    self.imgLegs = self.LRFListRight[self.LRFrame]

            if self.SwordAttack == True:
                self.imgArmTop = self.imgDict["AttackSwordRight"]
            else:
                self.imgArmTop = self.imgDict["SwordRight"]

            self.offsetTopArm[0] = self.SwordArmRightOffset[0]
            self.offsetTopArm[1] = self.SwordArmRightOffset[1]

            if self.aiming:
                if self.useMagicArm:
                    self.imgArmBottom = self.imgDict["SpellArm Right"]
                elif "Weapon" in self.equipment:
                    self.imgArmBottom = self.imgDict["RL Right"]
                else:
                    self.imgArmBottom = self.imgDict["FireArm Right"]

                self.offsetBottomArm[0] = self.offsetBottomArmRight[0]
                self.offsetBottomArm[1] = self.offsetBottomArmRight[1]
            
            # Arms

                # angle = math.degrees(-self.fireAngle)
                angle = math.degrees(-math.atan2(self.world.mouseWorld[1] - (self.pos[1] + self.dimens[1]/2), self.world.mouseWorld[0] - (self.pos[0] + self.dimens[0]/2)))
                originalSize = self.imgArmBottom.get_size()


                if self.world.mouseWorld[1] > (self.pos[1] + self.dimens[1]/2):
                    self.imgArmBottom = pygame.transform.rotate(self.imgArmBottom, angle)
                    # self.imgArmTop = pygame.transform.rotate(self.imgArmTop, angle)

                    self.offsetBottomArm[1] -= angle/15
                    # self.offsetTopArm[1] -= angle/15
                    self.offsetBottomArm[0] += angle/20
                    # self.offsetTopArm[0] += angle/20
                else:
                    self.imgArmBottom = pygame.transform.rotate(self.imgArmBottom, angle)
                    # self.imgArmTop = pygame.transform.rotate(self.imgArmTop, angle)

                    self.offsetBottomArm[1] = self.offsetBottomArm[1] + originalSize[1] - self.imgArmBottom.get_size()[1] - angle/15

                    # self.offsetTopArm[1] = self.offsetTopArm[1] + originalSize[1] - self.imgArmTop.get_size()[1] - angle/15
            else:
                if self.useMagicArm:
                    self.imgArmBottom = self.imgDict["SpellArmNoAim Right"]
                elif "Weapon" in self.equipment:
                    self.imgArmBottom = self.imgDict["RLNoAim Right"]
                else:
                    self.imgArmBottom = self.imgDict["FireArmNoAim Right"]

                # self.imgArmTop = self.imgDict["EmptyArm Right"]
                # self.offsetTopArm[0] = self.TopArmNoAimLeftOffSet [0]
                # self.offsetTopArm[1] = self.TopArmNoAimLeftOffSet [1]
                self.offsetBottomArm[0] = self.BottomArmNoAimRightOffSet[0]
                self.offsetBottomArm[1] = self.BottomArmNoAimRightOffSet[1]



        # Facing Left

        elif self.faceDir == "l":
            if self.showHitCounter.getState():
                self.imgBody = self.imgDict["DamFace Left"]
            elif self.SwordAttack:
                self.imgBody = self.imgDict["AttackFace Left"]
            elif self.aiming:
                self.imgBody = self.imgDict["AimingFace Left"]
            else:
                self.imgBody = self.imgDict["bodyLeft"]

            self.offsetLegs[0] = self.offsetLegsLeft[0]
            self.offsetLegs[1] = self.offsetLegsLeft[1]
            
            if self.momentum[0] == 0 and self.momentum[1] == 0:

                self.imgLegs = self.imgDict["LS Left"]

            else:
                self.imgLegs = self.LRFListLeft[self.LRFrame]

                if self.allowDown:
                    self.imgLegs = self.LRFListLeft[0]
                else:
                    self.imgLegs = self.LRFListLeft[self.LRFrame]

            if self.SwordAttack:
                self.imgArmBottom = self.imgDict["AttackSwordLeft"]
            else:
                self.imgArmBottom = self.imgDict["SwordLeft"]


            self.offsetBottomArm[0] = self.SwordArmLeftOffset[0]
            self.offsetBottomArm[1] = self.SwordArmLeftOffset[1]

            if self.aiming:
                if self.useMagicArm:
                    self.imgArmTop = self.imgDict["SpellArm Left"]
                elif "Weapon" in self.equipment:
                    self.imgArmTop = self.imgDict["RL Left"]
                else:
                    self.imgArmTop = self.imgDict["FireArm Left"]

                self.offsetTopArm[0] = self.offsetTopArmLeft[0]
                self.offsetTopArm[1] = self.offsetTopArmLeft[1]


                # Arms

                angle = math.degrees(math.atan2(self.world.mouseWorld[1] - (self.pos[1] + self.dimens[1]/2) , -( self.world.mouseWorld[0] - (self.pos[0] + self.dimens[0]/2))))
                # angle = math.degrees(-self.fireAngle)
                originalSize = self.imgArmTop.get_size()

                if self.world.mouseWorld[1] > (self.pos[1] + self.dimens[1]/2):


                    # self.imgArmBottom = pygame.transform.rotate(self.imgArmBottom, angle)
                    self.imgArmTop = pygame.transform.rotate(self.imgArmTop, angle)


                    # self.offsetBottomArm[1] += angle/15
                    self.offsetTopArm[1] += angle/15
                    # self.offsetBottomArm[0] = self.offsetBottomArm[0] + originalSize[0] - self.imgArmBottom.get_size()[0] + angle/15
                    self.offsetTopArm[0] = self.offsetTopArm[0] + originalSize[0] - self.imgArmTop.get_size()[0] + angle/15

                else:
                    # self.imgArmBottom = pygame.transform.rotate(self.imgArmBottom, angle)
                    self.imgArmTop = pygame.transform.rotate(self.imgArmTop, angle)

                    # self.offsetBottomArm[1] = self.offsetBottomArm[1] + originalSize[1] - self.imgArmBottom.get_size()[1] + angle/15

                    self.offsetTopArm[1] = self.offsetTopArm[1] + originalSize[1] - self.imgArmTop.get_size()[1] + angle/15

                    # self.offsetBottomArm[0] = self.offsetBottomArm[0] + originalSize[0] - self.imgArmBottom.get_size()[0] - angle/18
                    self.offsetTopArm[0] = self.offsetTopArm[0] + originalSize[0] - self.imgArmTop.get_size()[0] - angle/18
            else:
                # self.imgArmBottom = self.imgDict["EmptyArm Left"]
                if self.useMagicArm:
                    self.imgArmTop = self.imgDict["SpellArmNoAim Left"]
                elif "Weapon" in self.equipment:
                    self.imgArmTop = self.imgDict["RLNoAim Left"]
                else:
                    self.imgArmTop = self.imgDict["FireArmNoAim Left"]
                self.offsetTopArm[0] = self.TopArmNoAimLeftOffSet [0]
                self.offsetTopArm[1] = self.TopArmNoAimLeftOffSet [1]
                # self.offsetBottomArm[0] = self.offsetBottomArmLeft[0]
                # self.offsetBottomArm[1] = self.offsetBottomArmLeft[1]

        elif self.faceDir == "f":


            if self.momentum[0] == 0 and self.momentum[1] == 0:

                self.imgLegs = self.imgDict["WalkForward1"]

            else:
                self.imgLegs = self.WalkForwardList[self.LRFrame]

            self.offsetLegs[0] = self.offsetLegsForward[0]
            self.offsetLegs[1] = self.offsetLegsForward[1]

            if self.SwordAttack:
                self.imgBody = self.imgDict["AttackFaceForward"]
                self.imgArmBottom = self.imgDict["PistolForward"]
                self.imgArmTop = self.imgDict["AttackSwordForward"]
            else:
                self.imgBody = self.imgDict["bodyForward"]
                self.imgArmTop = self.imgDict["PistolForward"]
                self.imgArmBottom = self.imgDict["SwordForward"]
            self.offsetBottomArm[0] = self.WeaponsForwardOffset[0]
            self.offsetBottomArm[1] = self.WeaponsForwardOffset[1]
            self.offsetTopArm[0] = self.WeaponsForwardOffset[0]
            self.offsetTopArm[1] = self.WeaponsForwardOffset[1]



        elif self.faceDir == "b":
            self.imgBody = self.imgDict["bodyBack"]

            if self.momentum[0] == 0 and self.momentum[1] == 0:
                self.imgLegs = self.imgDict["WalkBack1"]

            else:
                self.imgLegs = self.WalkBackList[self.LRFrame]

            self.offsetLegs[0] = self.offsetLegsBack[0]
            self.offsetLegs[1] = self.offsetLegsBack[1]

            if self.SwordAttack:
                self.imgArmBottom = self.imgDict["AttackSwordBack"]
                self.imgArmTop = self.imgDict["PistolBack"]
                self.offsetBottomArm[0] = self.AttackSwordbackOffset[0]
                self.offsetBottomArm[1] = self.AttackSwordbackOffset[1]
            else:
                self.imgArmTop = self.imgDict["SwordBack"]
                self.imgArmBottom = self.imgDict["PistolBack"]
                self.offsetBottomArm[0] = self.WeaponsForwardOffset[0]
                self.offsetBottomArm[1] = self.WeaponsForwardOffset[1]

            self.offsetTopArm[0] = self.WeaponsForwardOffset[0]
            self.offsetTopArm[1] = self.WeaponsForwardOffset[1]


        # Beam Draw
        
        
        # if self.fireBeam == 1:



    def loadImages(self):
        self.imgDict = {
            # "bodyLeft": pygame.image.load("_IMAGES\Sprites\NPCs\Cassy\CharBodyLeft.png"),
            "bodyLeft": pygame.image.load("_IMAGES\Sprites\Player\LZT Left.png"),
            # "bodyRight": pygame.image.load("_IMAGES\Sprites\NPCs\Cassy\CharBodyRight.png"),
            "bodyRight": pygame.image.load("_IMAGES\Sprites\Player\LZT Right.png"),
            "AttackFace Left": pygame.image.load("_IMAGES\Sprites\Player\AttackFace Left.png"),
            "AttackFace Right": pygame.image.load("_IMAGES\Sprites\Player\AttackFace Right.png"),
            "AimingFace Left": pygame.image.load("_IMAGES\Sprites\Player\AimingFace Left.png"),
            "DamFace Left": pygame.image.load("_IMAGES\Sprites\Player\DamFaceLeft.png"),
            "AimingFace Right": pygame.image.load("_IMAGES\Sprites\Player\AimingFace Right.png"),
            "DamFace Right": pygame.image.load("_IMAGES\Sprites\Player\DamFaceRight.png"),
            "LS Right": pygame.image.load("_IMAGES\Sprites\Player\LS Right.png"),
            "LS Left": pygame.image.load("_IMAGES\Sprites\Player\LS Left.png"),
            "LR1 Right": pygame.image.load("_IMAGES\Sprites\Player\LR1 Right.png"),
            "LR1 Left": pygame.image.load("_IMAGES\Sprites\Player\LR1 Left.png"),
            "LR2 Right": pygame.image.load("_IMAGES\Sprites\Player\LR2 Right.png"),
            "LR2 Left": pygame.image.load("_IMAGES\Sprites\Player\LR2 Left.png"),
            "LR3 Right": pygame.image.load("_IMAGES\Sprites\Player\LR3 Right.png"),
            "LR3 Left": pygame.image.load("_IMAGES\Sprites\Player\LR3 Left.png"),
            "LR4 Right": pygame.image.load("_IMAGES\Sprites\Player\LR4 Right.png"),
            "LR4 Left": pygame.image.load("_IMAGES\Sprites\Player\LR4 Left.png"),
            "LR5 Right": pygame.image.load("_IMAGES\Sprites\Player\LR5 Right.png"),
            "LR5 Left": pygame.image.load("_IMAGES\Sprites\Player\LR5 Left.png"),
            "LR6 Right": pygame.image.load("_IMAGES\Sprites\Player\LR6 Right.png"),
            "LR6 Left": pygame.image.load("_IMAGES\Sprites\Player\LR6 Left.png"),
            "RL Right": pygame.image.load("_IMAGES\Sprites\Player\RLRight.png"),
            "FireArm Right": pygame.image.load("_IMAGES\Sprites\Player\FireArmRight.png"),
            "SpellArm Right": pygame.image.load("_IMAGES\Sprites\Player\SpellArmRight.png"),
            "RL Left": pygame.image.load("_IMAGES\Sprites\Player\RLLeft.png"),
            "FireArm Left": pygame.image.load("_IMAGES\Sprites\Player\FireArmLeft.png"),
            "SpellArm Left": pygame.image.load("_IMAGES\Sprites\Player\SpellArmLeft.png"),
            "EmptyArm Right": pygame.image.load("_IMAGES\Sprites\Player\EmptyArmRight.png"),
            "EmptyArm Left": pygame.image.load("_IMAGES\Sprites\Player\EmptyArmLeft.png"),
            "SpellArmNoAim Left": pygame.image.load("_IMAGES\Sprites\Player\SpellArmNoAimLeft.png"),
            "FireArmNoAim Left": pygame.image.load("_IMAGES\Sprites\Player\FireArmNoAimLeft.png"),
            "RLNoAim Left": pygame.image.load("_IMAGES\Sprites\Player\RLNoAimLeft.png"),
            "SpellArmNoAim Right": pygame.image.load("_IMAGES\Sprites\Player\SpellArmNoAimRight.png"),
            "FireArmNoAim Right": pygame.image.load("_IMAGES\Sprites\Player\FireArmNoAimRight.png"),
            "RLNoAim Right": pygame.image.load("_IMAGES\Sprites\Player\RLNoAimRight.png"),
            "SwordLeft": pygame.image.load("_IMAGES\Sprites\Player\SwordLeft.png"),
            "SwordRight": pygame.image.load("_IMAGES\Sprites\Player\SwordRight.png"),
            "AttackSwordRight": pygame.image.load("_IMAGES\Sprites\Player\AttackSwordRight.png"),
            "AttackSwordLeft": pygame.image.load("_IMAGES\Sprites\Player\AttackSwordLeft.png"),
            "bodyForward": pygame.image.load("_IMAGES\Sprites\Player\LookForward.png"),
            "AttackFaceForward": pygame.image.load("_IMAGES\Sprites\Player\AttackFaceForward.png"),
            "bodyBack": pygame.image.load("_IMAGES\Sprites\Player\LookBack.png"),
            "WalkBack1": pygame.image.load("_IMAGES\Sprites\Player\WalkBack1.png"),
            "WalkBack2": pygame.image.load("_IMAGES\Sprites\Player\WalkBack2.png"),
            "WalkBack3": pygame.image.load("_IMAGES\Sprites\Player\WalkBack3.png"),
            "WalkBack4": pygame.image.load("_IMAGES\Sprites\Player\WalkBack4.png"),
            "WalkBack5": pygame.image.load("_IMAGES\Sprites\Player\WalkBack5.png"),
            "WalkBack6": pygame.image.load("_IMAGES\Sprites\Player\WalkBack6.png"),
            "WalkBack7": pygame.image.load("_IMAGES\Sprites\Player\WalkBack7.png"),
            "WalkForward1": pygame.image.load("_IMAGES\Sprites\Player\WalkForward1.png"),
            "WalkForward2": pygame.image.load("_IMAGES\Sprites\Player\WalkForward2.png"),
            "WalkForward3": pygame.image.load("_IMAGES\Sprites\Player\WalkForward3.png"),
            "WalkForward4": pygame.image.load("_IMAGES\Sprites\Player\WalkForward4.png"),
            "WalkForward5": pygame.image.load("_IMAGES\Sprites\Player\WalkForward5.png"),
            "WalkForward6": pygame.image.load("_IMAGES\Sprites\Player\WalkForward6.png"),
            "WalkForward7": pygame.image.load("_IMAGES\Sprites\Player\WalkForward7.png"),
            "WeaponsForward": pygame.image.load("_IMAGES\Sprites\Player\WeaponsForward.png"),
            "WeaponsBack": pygame.image.load("_IMAGES\Sprites\Player\WeaponsBack.png"),
            "SwordBack": pygame.image.load("_IMAGES\Sprites\Player\SwordBack.png"),
            "PistolBack": pygame.image.load("_IMAGES\Sprites\Player\PistolBack.png"),
            "SwordForward": pygame.image.load("_IMAGES\Sprites\Player\SwordForward.png"),
            "AttackSwordForward": pygame.image.load("_IMAGES\Sprites\Player\AttackSwordForward.png"),
            "AttackSwordBack": pygame.image.load("_IMAGES\Sprites\Player\AttackSwordBack.png"),
            "PistolForward": pygame.image.load("_IMAGES\Sprites\Player\PistolForward.png"),
            "WeaponsForwardBottom": pygame.image.load("_IMAGES\Sprites\Player\WeaponsForwardBottom.png"),

        }

        for i in self.imgDict:
            self.imgDict[i] = self.imgDict[i].convert_alpha()

        self.imgBody = self.imgDict["bodyRight"]

        self.LRFListRight = [self.imgDict["LR1 Right"], self.imgDict["LR2 Right"], self.imgDict["LR3 Right"],
                             self.imgDict["LR4 Right"], self.imgDict["LR5 Right"], self.imgDict["LR6 Right"]]
        self.LRFListLeft = [self.imgDict["LR1 Left"], self.imgDict["LR2 Left"], self.imgDict["LR3 Left"],
                            self.imgDict["LR4 Left"], self.imgDict["LR5 Left"], self.imgDict["LR6 Left"]]
        self.WalkBackList = [self.imgDict["WalkBack6"], self.imgDict["WalkBack2"], self.imgDict["WalkBack3"],
                             self.imgDict["WalkBack7"], self.imgDict["WalkBack4"], self.imgDict["WalkBack5"]]
        self.WalkForwardList = [self.imgDict["WalkForward2"], self.imgDict["WalkForward6"],
                                self.imgDict["WalkForward3"], self.imgDict["WalkForward4"],
                                self.imgDict["WalkForward7"], self.imgDict["WalkForward5"]]

        self.imgLegs = self.imgDict["LS Right"]

        self.imgArmBottom = self.imgDict["FireArm Right"]
        self.imgArmTop = self.imgDict["EmptyArm Right"]

    def loadAudio(self):
        self.audio = audioMan.SoundController()

        soundPaths = os.listdir("_AUDIO\\FX\\Player")
        for i in range(0, len(soundPaths)):
            soundPaths[i] = "_AUDIO\\FX\\Player\\" + soundPaths[i]

        self.audio.loadFromPaths(soundPaths, .5)


    def reload(self):
        self.loadImages()
        self.loadAudio()

        #Stuff For Updates

    def sanitizeForPickling(self):
        del self.imgDict
        del self.imgBody
        del self.LRFListRight
        del self.LRFListLeft
        del self.WalkBackList
        del self.WalkForwardList
        del self.imgLegs
        del self.imgArmBottom
        del self.imgArmTop
        self.inputTracker = {"w": False, "s": False, "a": False, "d": False, "space": False, "shift": False}
        self.audio.silenceAll()
        del self.audio