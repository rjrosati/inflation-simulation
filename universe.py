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
c = 100
num_dt=0
t=0
done = False
paused = True
light_traveling = False
WHITE = (255,255,255)
BLACK = (  0,  0,  0)

H = 1E-2
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

def blit_txt_with_outline(screen, loc, font, text, fg_color, bg_color,thk):
        textfg = font.render(text,True, fg_color)
        textbg = font.render(text,True, bg_color)
        screen.blit(textbg,loc+(-thk,-thk))
        screen.blit(textbg,loc+( thk,-thk))
        screen.blit(textbg,loc+(-thk, thk))
        screen.blit(textbg,loc+( thk, thk))
        screen.blit(textfg,loc)
        return


while not done:
    screen.fill(BLACK)
    if not paused:
        num_dt+=1
        t = num_dt*dt
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c and light_traveling == False:
            light_traveling = True
            tc = t
            td = t+1


    if (num_dt%dt_per_frame==0):
        grid = recompute_grid(t,uniWidth/2,uniHeight/2)
        for square in grid:
            pygame.draw.rect(screen,WHITE,square,1)

        if light_traveling:
            if (tc <= t <= td):
                # this radius should be a more complicated function of time
                r = int(c*(t-tc))
                pygame.draw.circle(screen,(255,255,0),(int(uniWidth/2),int(uniHeight/2)),r,0 if r<5 else 5 )
            else:
                light_traveling = False

        blit_txt_with_outline(screen,(20,20),font,"t = %6.4f"%t,WHITE,BLACK,3)
        blit_txt_with_outline(screen,(20,50),font,"a(t) = %3.2f"% a(t),WHITE,BLACK,3)


        pygame.display.flip() 
        clock.tick(maxfps)
