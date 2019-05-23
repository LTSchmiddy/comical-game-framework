import imageio

import pygame, time
screen = pygame.display.set_mode([1900, 1060])

from moviepy.editor import *





pygame.display.set_caption('Hello World!')

clip = VideoFileClip('P&R710.mp4').without_audio()

img = clip.get_frame(1)

clip.blit_on(screen, 1)
pygame.display.flip()

# clip.preview()

pygame.quit()
time.sleep(5)
exit()