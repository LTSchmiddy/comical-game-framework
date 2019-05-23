import pygame, json, os, random

ExpFilePath = "EnvironmentData/_EXP/0_0.json"

expGridSize = [20, 20]

grid = []

for j in range(0, expGridSize[1]):
    grid.append([])
    for i in range(0, expGridSize[0]):
        point = random.random()
        if point < .3:
            grid[j].append(1)
        else:
            grid[j].append(0)





# Block Generation:
envData = json.load(open(ExpFilePath, "r"))
envData["Objects"] = {}

for j in range(0, expGridSize[1]):
    for i in range(0, expGridSize[0]):
        if grid[j][i] == 1:
            envData["Objects"].update({
                "Floor " + str(j) + " " + str(i): {
                    "useMultPos": 32,
                    "useMultDimens": 32,
                    "pos": [i*15, j*5],
                    "dimens": [15, 5],
                    "useTemplate": "BackWall1"
                }
            })
        else:
            envData["Objects"].update({
                "Floor " + str(j) + " " + str(i): {
                    "type": "EnvShuffleImageBg",
                    "useMultPos": 32,
                    "useMultDimens": 32,
                    "pos": [i * 15, j * 5],
                    "dimens": [15, 5],
                    "useTemplate": "OutdoorGrass1"
                }
            })

json.dump(envData, open(ExpFilePath, "w"), indent=4, sort_keys=True)

exit()