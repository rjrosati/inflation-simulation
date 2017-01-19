import math
import sys
import pygame
import numpy as np
from scipy.special import jv

import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
from pygame.locals import *
import matplotlib.pyplot as plt

matplotlib.style.use('dark_background')

uniWidth = 900
uniHeight = 900

pygame.init()
screen = pygame.display.set_mode((uniWidth,uniHeight))
clock = pygame.time.Clock()
maxfps=60
font = pygame.font.Font(None,30)
dt=0.01
dt_per_frame = 1
c = 5
num_dt=0
t=0
done = False
paused = True
light_traveling = False
WHITE = (255,255,255)
GREEN = (  0,255,  0)
BLACK = (  0,  0,  0)

H = 1E-1
# for now, de Sitter expansion
def a(t):
    return np.exp(H*t)


blk = 20
def recompute_grid(t,center_x,center_y):
    # create a square grid, comoving
    grid = []
    a1 = a(t)
    w,h,b = uniWidth,uniHeight,blk
    ws,hs = 0,0
    while a1 > w/b:
        #rescale grid when no longer visible
        a1 /= w/b
    for x in range(ws,w,b):
        for y in range(hs,h,b):
            grid.append(pygame.Rect(a1*(x-center_x)+center_x,a1*(y-center_y)+center_y,a1*b,a1*b))
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

drawing_plot = True
#t_range=[]
#at_range=[]
#fig = plt.figure(figsize=[4, 2], dpi=100)
#ax = fig.gca()
#ax.set_xlim([0,100])
#ax.set_ylim([0,50])
#canvas = agg.FigureCanvasAgg(fig)
#renderer = canvas.get_renderer()
#psize = canvas.get_width_height()
p_loc = np.array((uniWidth/2,0))
p_shape  = np.array((400,200))
xlim = np.array((0,100))
ylim = np.array((0,50))
points = [] 
def draw_plot(screen):
    #ax.plot(t_range, at_range,'c')
    #canvas.draw()
    #screen.blit(pygame.image.fromstring(renderer.tostring_rgb(), psize, "RGB"),(uniWidth/2,0))
    if len(points)>1:
        pygame.draw.lines(screen, GREEN, False, points, 1)
    return

while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            drawing_plot = not drawing_plot
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            light_traveling = True
            tc = t
            td = t+100
            r=0

    if not paused:
        num_dt+=1
        t = num_dt*dt
        points.append(p_loc + (0,+p_shape[1]) + (t/xlim[1]*p_shape[0], -a(t)/ylim[1]*p_shape[1]))

        if light_traveling:
            if (tc <= t <= td):
                v = c + H*r
                r += v*dt
            else:
                light_traveling = False

        if (num_dt%dt_per_frame==0):
            screen.fill(BLACK)
            grid = recompute_grid(t,uniWidth/2,uniHeight/2)
            for square in grid:
                pygame.draw.rect(screen,WHITE,square,1)

            if light_traveling:
                    pygame.draw.circle(screen,(255,255,0),(int(uniWidth/2),int(uniHeight/2)),int(r),0 if r<5 else 5 )

            blit_txt_with_outline(screen,(20,20),font,"t = %6.4f"%t,WHITE,BLACK,3)
            blit_txt_with_outline(screen,(20,50),font,"a(t) = %3.2f"% a(t),WHITE,BLACK,3)

            if drawing_plot:
                draw_plot(screen)

            pygame.display.flip() 
            clock.tick(maxfps)
