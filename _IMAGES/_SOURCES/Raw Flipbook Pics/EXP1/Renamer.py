import os
value = 0
for i in os.listdir(os.getcwd()):
	if i != "Renamer.py":
		print "expIMG" + str(value)
		os.rename(i, "expIMG" + str(value) + ".png")
		value += 1