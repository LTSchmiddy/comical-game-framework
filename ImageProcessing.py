import pygame, os

pygame.init()

imagePath = "_IMAGES\\Sprites\\EnemyTypes\\Skeleton 1\\SkeletonTileSheet.png"
outPath = "_IMAGES\\Sprites\\EnemyTypes\\Skeleton 1\\OUTSkeletonTileSheet.png"



# Start Execution:
myImage = pygame.image.load(imagePath)

for x in range(0, myImage.get_width()):
    for y in range(0, myImage.get_height()):
        myColor = myImage.get_at([x, y])
        if (myColor.r + myColor.g + myColor.b)/3 > 127:
            myColor = pygame.Color(255, 255, 255, myColor.a)
        else:
            myColor = pygame.Color(0, 0, 0, myColor.a)
        myImage.set_at([x, y], myColor)


pygame.image.save(myImage, outPath)