import Launcher, sys
if "--useLauncher" in sys.argv:
    Launcher.loadLauncher()


import MainGamePanel, StatBar, InGameMenu, ShoppingMenu, DialogScreen, PauseMenu, MainMenu, DebugConsole, NotificationArea, FlipBookViewer, HotBar, WeapHUD, RLM

# modules = [[MainGamePanel, [1920,1080], [0, 0]], [StatBar, [600,150], [20, 20]], [InGameMenu, [1880,860], [20, 200]], [ShoppingMenu, [1880,860], [20, 200]], [DialogScreen, [1880,360], [20, 700]], [PauseMenu, [500,700], [110, 225]], [MainMenu, [500,700], [110, 225]], [DebugConsole, [1880,1040], [20, 20]], [NotificationArea, [550,100], [1320, 20]], [FlipBookViewer, [1920,1080], [0, 0]]]
modules = [[MainGamePanel], [StatBar], [WeapHUD], [RLM], [InGameMenu], [HotBar], [DialogScreen], [ShoppingMenu], [PauseMenu], [MainMenu], [DebugConsole], [NotificationArea], [FlipBookViewer]]

# dispdims = [1920, 1080]



#***********DO_NOT_TOUCH_THIS_LINE**************

#The content above can be re-written by "Start_HUB.py".
#The "disp_config.txt" file is the easiest way to configure the panels used in this file.
#In that file, define the panel modules, their dimension arguments, and their position arguements.
#Then Run "Start_HUB.py". It will update the information above to reflect "disp_config.txt".

import pygame, os, time, thread, dataManagers, gameSettingsMaster
from dataManagers import audioMan, dialogManager, flipBookHandler, debugLogging, steamWrapper, storeManager, saveManager

mainSettings = gameSettingsMaster.getSettingsDict()

displaySettings = mainSettings["Display"]
useFPSStabilizing = displaySettings["Use Frame Stabilizing"]

screenSettings = gameSettingsMaster.getScreenSettings(displaySettings["DisplayFile"])

dispdims = screenSettings["Screen Resolution"]

for i in range(0, len(modules)):
    useName = str(modules[i][0].__name__)
    modules[i].append(screenSettings["Panel Settings"][useName]["res"])
    modules[i].append(screenSettings["Panel Settings"][useName]["pos"])
    modules[i].append(screenSettings["Panel Settings"][useName])


# Loading Steam API:

# run Visual Studio dev version of the API wrapper:
steamAPI = steamWrapper.API(True)


isSteamLoaded = steamAPI.initSteam()
print steamAPI.getSpam()


from EngineControl import flipAnim
#
# import OpenGL.GL
# import OpenGL.GLU
pygame.init()
pygame.mixer.init()

gfxFPS = displaySettings["Frames Per Second"]

pygame.display.set_caption("Comical - v0.1")
pygame.display.set_icon(pygame.image.load("Icon.png"))



if (displaySettings["Fullscreen"]):
        screen = pygame.display.set_mode(dispdims, pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE)
        # screen = pygame.display.set_mode(dispdims, pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.OPENGL|pygame.HWSURFACE )
else:
    screen = pygame.display.set_mode(dispdims, pygame.DOUBLEBUF | pygame.RESIZABLE)
    # screen = pygame.display.set_mode(dispdims, pygame.DOUBLEBUF|pygame.OPENGL)

useGFXThread = False
if "--useGFXThread" in sys.argv:
    useGFXThread = True
    print "Using Seperate Graphics Thread!"


#
# useWrapperServer = False
# if "--useWrapperServer" in sys.argv:
#     useWrapperServer = True
#     print "Using Wrapper Server!"
# else:
#     print "Wrapper Server Disabled!"

if "--FPS" in sys.argv:
    gfxFPS = int(sys.argv[sys.argv.index("--FPS") + 1])
    print "FPS Set to", gfxFPS
    time.sleep(1)


fpsFactor = int(60/gfxFPS)
# print fpsFactor
flipCounter = fpsFactor

audio = audioMan.AudioController()

# Initialize Loading Screen. Automatically appears if the main loop is taking too long.
canUseLoadingScreen = False
isLoading = False
lastFrameUpdate = 0
loadingAnim = flipAnim.Animation(1)
loadingAnim.loadFramesFromFolder("_IMAGES/SplashScreen/LoadingAnim", ".png")
def LoadingScreenThread():
    global lastFrameUpdate, isLoading
    splash = pygame.image.load("_IMAGES/SplashScreen/SiteLogoTab_v3.png")
    # screen.fill([0, 0, 0])
    # screen.blit(splash, [(screen.get_size()[0] / 2) - (splash.get_size()[0] / 2),
    #                      (screen.get_size()[1] / 2) - (splash.get_size()[1] / 2)])
    try:
        while True:
            if pygame.time.get_ticks() - lastFrameUpdate > 300 and not isLoading:
                isLoading = True
                loadingAnim.currentFrame = 0


            if isLoading and canUseLoadingScreen:
                screen.fill([0, 0, 0])
                splash = loadingAnim.getFrame()
                screen.blit(splash, [(screen.get_size()[0] / 2) - (splash.get_size()[0] / 2),
                                     (screen.get_size()[1] / 2) - (splash.get_size()[1] / 2)])
                pygame.display.flip()

            pygame.time.delay(200)
    except Exception as ex:
        template = "An exception of type {0} occurred:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message

thread.start_new_thread(LoadingScreenThread, ())

inIntro = True
def LogoIntro():
    global  canUseLoadingScreen, inIntro
    if not "--SkipLogo" in sys.argv:
        screen.fill([255,255,255])
        splash = pygame.image.load("_IMAGES\\SplashScreen\\SiteLogoTab_v3.png")
        # screen.fill([0, 0, 0])
        screen.blit(splash, [(screen.get_size()[0]/2) - (splash.get_size()[0]/2), (screen.get_size()[1]/2) - (splash.get_size()[1]/2)])
        pygame.display.flip()

        channela = audio.triggerSound("AngelFishJingle")
        time.sleep(4)
    canUseLoadingScreen = True
    inIntro = False
    # audio.setMusicTrack("MainTheme")

thread.start_new_thread(LogoIntro, ())






hostvar = {
    "DebugStart":False,
    "Game Paused":True,
    "Show Pause Menu":False,
    "Show Status Menu":False,
    "Player Weapon Energy":100,
    "Player Weapon Energy Max":100,
    "Player Magic":100,
    "Player Magic Max":100,
    "Player Health":100,
    "Player Health Max":100,
    "Player Weapon Name":"Pulse Laser",
    "Developer Mode":False,
    "Game Env": None,
    "Game Notif": dataManagers.NotificationHandler.Handler(True),
    "masterAudio": audio,
    "dialogM": dialogManager.dialogManager(),
    "flipbookM": flipBookHandler.FlipbookManager(),
    "steamAPI": steamAPI,
    "debugLogging": debugLogging.Logger(False),
    "storeManager": storeManager.StoreManager(),
    "saveM": saveManager.SaveManager()
}





#startup loop:



panels = []

for i in range(0, len(modules)):
    modules[i][3]["hostVar"] = hostvar

for mod in modules:


    n = mod[0].GUI(mod[1], mod[2], mod[3])
#    n.updatePanel()
    panels.append(n)

# print panels

clockLogic = pygame.time.Clock()
clockGFX = pygame.time.Clock()

for i in panels:
    screen.blit(i.Panel, i.pos)
# pygame.display.flip()





def GFXThread (myPanels):
    global allowFlip
    print "THREAD2"
    # for i in myPanels:
    #     i.get_hostvar(hostvar)

    while True:
        pygame.display.flip()
        clockGFX.tick(gfxFPS)

# if useGFXThread:
#     thread.start_new_thread(GFXThread, (panels))

# Handle Communication with the Steam Wrapper:


# def serveWrapper ():
#     serverClass = wrapperCMD.wrapperServer()
#     cherrypy.server.socket_port = 25397
#     cherrypy.quickstart(serverClass)
#
#
# if useWrapperServer:
#     thread.start_new_thread(serveWrapper, ())

drawingPanels = 0

def panelDrawThread(i, ext):
    global drawingPanels

    drawingPanels += 1

    if i.show:
        if i.get_updatePanel():
            i.updatePanel()
        screen.blit(i.Panel, i.pos)

    drawingPanels -= 1


def panelDraw(Panel):
    thread.start_new_thread(panelDrawThread, (Panel, "hi"))

def flipOnThread():
    thread.start_new_thread(pygame.display.flip, ())





keyheldlist = []
# while not os.path.isfile("kill"):

while inIntro:
    pass

while True:
    flipCounter += 1

    # print flipCounter
    if flipCounter >= fpsFactor:
        flipCounter = 0
        # print "Tick!"



    
#GET EVENTS    
    event_list = pygame.event.get()
    
    kdnlist = []
    kuplist = []

    mouseDownList = []
    mouseUpList = []

    mouseaction = list(pygame.mouse.get_pressed())
    mouseaction.append(0)

    for event in event_list: 
        if event.type == pygame.QUIT:

            exit()
        elif event.type == pygame.KEYDOWN:
            kdnlist.append(event.key)
            keyheldlist.append(event.key)
                
        elif event.type == pygame.KEYUP:
            kuplist.append(event.key)
            keyheldlist.remove(event.key)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                mouseaction[3] = (1)

            elif event.button == 5:
                mouseaction[3] = (-1)

            mouseDownList.append(event.button)

        elif event.type == pygame.MOUSEBUTTONUP:
            mouseUpList.append(event.button)

    if (pygame.K_RALT in keyheldlist or pygame.K_LALT in keyheldlist) and pygame.K_F4 in keyheldlist:
        exit()
             
    # pygame.event.clear()
    # if kdnlist != []:
    #     print kdnlist


    screen.fill([25, 25, 25])
#RUN EACH PANEL  
    for i in panels:

        i.get_hostvar(hostvar)
        i.bg_tasks()


        i.event_loop({"kdown":kdnlist, "kup":kuplist, "kheld":keyheldlist, "mdown":mouseDownList, "mup":mouseUpList, "mstate":mouseaction})
        hostvar = i.send_hostvar()
        
        
        # if useGFXThread == False:
        if flipCounter == 0:
            # panelDraw(i)
            #
            if i.show:
                if i.get_updatePanel():
                    i.updatePanel()

                screen.blit(i.Panel, i.pos)
            #
            #


    # print flipCounter
    if flipCounter == 0:

        while drawingPanels != 0:
            pass

        pygame.display.flip()
        fpsFactor = int(60 / gfxFPS)
        # print "Flip"





    clockLogic.tick(60)
    if useFPSStabilizing:
        currentFPS = clockLogic.get_fps()
        if currentFPS > 0:
            # print currentFPS
            fpsFactor = int(60/currentFPS)

    lastFrameUpdate = pygame.time.get_ticks()

    isLoading = False

    
        