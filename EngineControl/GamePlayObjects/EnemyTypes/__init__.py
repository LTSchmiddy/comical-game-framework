import os, Shade

# __all__ = ["Shade"]
loadMod = ["Shade"]

for i in os.listdir("EngineControl\\GamePlayObjects\\EnemyTypes"):
    if i != "__init__.py" and i.split(".")[1] == "py":
        loadMod.append(i.split(".")[0])

__all__ = loadMod