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
dt_per_frame = 10
c = 1
t=0
done = False
paused = False

H = 1E-3
# for now, de Sitter expansion
def a(t):
    return np.exp(H*t)

blk = 100
def recompute_grid(t,center_x,center_y):
    # create a square grid, comoving
    grid = []
    a1 = a(t)
    for x in range(0,uniWidth,blk):
        for y in range(0,uniHeight,blk):
            grid.append(pygame.Rect(a1*(x-center_x)+center_x,a1*(y-center_y)+center_y,a1*blk,a1*blk))
    return grid


while not done:
    screen.fill((0,0,0))
    if not paused:
        t+=1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused




    if (t%dt_per_frame==0):
        grid = recompute_grid(t,uniWidth/2,uniHeight/2)
        for square in grid:
            pygame.draw.rect(screen,(255,255,255),square,1)


        #pygame.draw.circle(

        text = font.render("t = %6.4f"%(t*dt), True, (255,255,255))
        textbk = font.render("t = %6.4f"%(t*dt), True, (0,0,0))
        screen.blit(textbk,(19,19))
        screen.blit(textbk,(19,21))
        screen.blit(textbk,(21,19))
        screen.blit(textbk,(21,21))
        screen.blit(text,(20,20))
        pygame.display.flip()
        clock.tick(maxfps)
