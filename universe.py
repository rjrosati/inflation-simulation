import math
import pygame
import numpy as np

uniWidth = 900
uniHeight = 900

pygame.init()
screen = pygame.display.set_mode((uniWidth,uniHeight))
clock=pygame.time.Clock()
maxfps=60
font = pygame.font.Font(None,30)
dt=0.05
dt_per_frame = 1
c = 1


t=0
while True:
  screen.fill((0,0,0))
  t+=dt
  
  if (t%dt_per_frame==0):
      for massPoint in massPoints:
        massPoint.render()
      text = font.render("t = %6.4f"%(t*dt), True, (255,255,255))
      screen.blit(text,(20,20))
      pygame.display.flip()
      clock.tick(maxfps)
