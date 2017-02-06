import math
import sys
import pygame
import numpy as np
import random

fontpath = "./PressStart2P.ttf" 
uniWidth = 900
uniHeight = 900
blk = 100
pygame.init()
screen = pygame.display.set_mode((uniWidth,uniHeight), pygame.FULLSCREEN)
clock = pygame.time.Clock()
maxfps=60
font = pygame.font.Font(fontpath,20)
bigfont = pygame.font.Font(fontpath,30)
dt = 0.01
dt_per_frame = 1
c=10
num_dt=0
t=0
pausex=0
done=False
paused=True
godmode=False
light_traveling=False
lights_traveling=False
horizons=True
music = False 
WHITE = (255,255,255)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
YELLOW= (255,255,  0)
CYAN  = (  0,255,255)
MAGENTA=(255,  0,255)
BLACK = (  0,  0,  0)
q=1

colors = [WHITE,RED,GREEN,BLUE,YELLOW,CYAN,MAGENTA,BLACK]

H0 = 1E-1
def infla(t):
    return np.exp(H0*t)
def rad(t):
    return (2*H0*t)**0.5 # (should this be / 2 ?)
def radH(t):
    return H0 * a(t)**(-2)

def particle_horizon(tc,t):
    if godmode:
        return c/H0*np.exp(-H0*tc)
    else: return a(t)*c/H0*np.exp(-H0*tc)
def max_causal_horizon(godmode):
    if godmode:
        return c/H
    else: return c/H*a(t)

def recompute_grid(t,center_x,center_y,a1):
    # create a square grid, comoving
    grid = []
    w,h,b = uniWidth,uniHeight,blk
    ws,hs = 0,0
    #rescale grid when no longer visible
    while a1 > w/b:
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
p_shape  = np.array((400,200),dtype=int)
p_loc = np.array((uniWidth-(p_shape[0]+50),50),dtype=int)
xlim = np.array((0,100),dtype=int)
ylim = np.array((0,50),dtype=int)
points = [] 
ticksize = 10
axiscolor = CYAN
plotcolor = GREEN
ylabel = "a(t)"
xlabel = "t"
def draw_plot(screen):
    # draw background
    pygame.draw.rect(screen, BLACK,(p_loc[0],p_loc[1],p_shape[0],p_shape[1]))
    # x axis and ticks
    pygame.draw.line(screen, axiscolor,(p_loc[0],p_loc[1]+p_shape[1]),(p_loc[0]+p_shape[0],p_loc[1]+p_shape[1]), 3)
    for x in range(p_loc[0],p_shape[0]+p_loc[0],40):
        pygame.draw.line(screen, axiscolor,(x,p_loc[1]+p_shape[1]),(x,p_loc[1]+p_shape[1]-ticksize))
    # y axis and ticks
    pygame.draw.line(screen, axiscolor,(p_loc[0],p_loc[1]),(p_loc[0],p_loc[1]+p_shape[1]), 3)
    for y in range(p_loc[1],p_shape[1]+p_loc[1],40):
        pygame.draw.line(screen, axiscolor,(p_loc[0],y),(p_loc[0]+ticksize,y))
    # axis labels
    text = font.render(xlabel,True,WHITE,BLACK)
    screen.blit(text, p_loc + p_shape + (-3*ticksize,-3*ticksize))
    text = font.render(ylabel,True,WHITE,BLACK)
    screen.blit(text, p_loc + (3*ticksize,2*ticksize))

    # curve
    if len(points)>1:

        pygame.draw.lines(screen, plotcolor, False, points, 3)
        if ((points[-1][0] > p_loc[0] + p_shape[0]) or (points[-1][1] < p_loc[1])):
            blit_txt_with_outline(screen,(250,850),font,"INFLATION IS OFF THE CHARTS!!",WHITE,BLACK,3)

    return

fast = False
godgrid = recompute_grid(t,uniWidth/2,uniHeight/2,1)
a = lambda t: infla(t)
H = lambda t: H0
inflating = True
pygame.mixer.init()
pygame.mixer.music.load('keygen_music.mp3')
pygame.mixer.music.play(loops=-1)
music = True
while not done:
    keys = pygame.key.get_pressed()    
    if keys[pygame.K_RETURN]:
        fast = True
    else:
        fast = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if light_traveling:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos2 = pygame.mouse.get_pos()
                pos2 = (pos2-np.array((uniWidth/2,uniHeight/2)))/(a(t)/q)+np.array((uniWidth/2,uniHeight/2))
                lights_traveling = True
                tc = t
                td = t+100
                r=0
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos1 = pygame.mouse.get_pos()
                pos1 = (pos1-np.array((uniWidth/2,uniHeight/2)))/(a(t)/q)+np.array((uniWidth/2,uniHeight/2))
                light_traveling = True
                tc = t
                td = t+100
                r=0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done=True
            if event.key == pygame.K_p:
                drawing_plot = not drawing_plot
            if event.key == pygame.K_SPACE:
                paused = not paused
                pauset=0
            if event.key == pygame.K_g:
                godmode = not godmode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if not music:
                    pygame.mixer.init()
                    pygame.mixer.music.load('keygen_music.mp3')
                    pygame.mixer.music.play(loops=-1)
                    music = True
                else:
                    pygame.mixer.music.stop()
                    music = False
            if event.key == pygame.K_h:
                horizons = not horizons
            if event.key == pygame.K_e and inflating:
                # let's end inflation, switch a(t) to a different function
                inflating = False
                tswitch = t
                a = lambda t: infla(tswitch) + rad(t-tswitch)
                H = lambda t: radH(t)
                horizons = False
            if event.key == pygame.K_r:
                #reset to the beginning
                inflating = True
                light_traveling = False
                lights_traveling = False
                horizons = True 
                num_dt = 0
                a = lambda t: infla(t)
                H = lambda t: H0
                points = []






    if not paused:
        if fast:
            num_dt+=10
        else:
            num_dt+=1

        t = num_dt*dt
        points.append(p_loc + (0,+p_shape[1]) + (t/xlim[1]*p_shape[0], -a(t)/ylim[1]*p_shape[1]))
        if light_traveling:
            if (tc <= t <= td):
                v = c + H(t)*r
                if fast:
                    r+= v*10*dt
                else:
                    r += v*dt
            else:
                light_traveling = False

        if (num_dt%dt_per_frame==0):
            screen.fill(BLACK)
            if godmode:
                q = a(t)
                grid = godgrid
            else:
                q = 1
                grid = recompute_grid(t,uniWidth/2,uniHeight/2,a(t))

            for square in grid:
                pygame.draw.rect(screen,WHITE,square,1)

            if light_traveling:
                pos1_tmp = np.array((uniWidth/2,uniHeight/2)) + (pos1-np.array((uniWidth/2,uniHeight/2)))*a(t)/q
                pygame.draw.circle(screen,YELLOW,(int(pos1_tmp[0]),int(pos1_tmp[1])),int(r/q),0 if int(r/q)<5 else 5 )
                if horizons:
                    h = particle_horizon(tc,t)
                    pygame.draw.circle(screen,RED,(int(pos1_tmp[0]),int(pos1_tmp[1])),int(h),0 if int(h)<5 else 5 )
                if lights_traveling:
                    pos2_tmp = np.array((uniWidth/2,uniHeight/2)) + (pos2-np.array((uniWidth/2,uniHeight/2)))*a(t)/q
                    pygame.draw.circle(screen,BLUE,(int(pos2_tmp[0]),int(pos2_tmp[1])),int(r/q),0 if int(r/q)<5 else 5 )
                    if horizons:
                        h = particle_horizon(tc,t)
                        pygame.draw.circle(screen,RED,(int(pos2_tmp[0]),int(pos2_tmp[1])),int(h),0 if int(h)<5 else 5 )


            blit_txt_with_outline(screen,(20,20),font,"t = %6.4f"%t,WHITE,BLACK,3)
            blit_txt_with_outline(screen,(20,50),font,"a(t) = %3.2f"% a(t),WHITE,BLACK,3)

            if drawing_plot:
                draw_plot(screen)


            pygame.display.flip() 
            clock.tick(maxfps)
    else:

        # show instructions
        screen.fill(BLACK)
        fun_color = random.choice(colors)
        wletters = "...o0o0o TEAM LHS=RHS o0o0o..."
        i=0
        for letter in wletters:
            y = 120+30*np.sin(2*np.pi/(uniWidth/2)*(pausex+i*30))
            x = pausex+i*30
            x %= uniWidth
            i += 1
            text = bigfont.render(letter,True,fun_color)
            screen.blit(text,(x,y))


        text = bigfont.render("INFLATION SIMULATOR 9000",True, fun_color)
        text_rect = text.get_rect(center=(int(uniWidth/2),50))
        screen.blit(text,text_rect)

        text = font.render("CLICK    release light beams",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10)-30,top=int(uniHeight/4)+50)
        screen.blit(text,text_rect)
        
        text = font.render("p    display a(t) plot",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10),top=int(uniHeight/4)+100)
        screen.blit(text,text_rect)

        text = font.render("h    display particle horizon",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10),top=int(uniHeight/4)+150)
        screen.blit(text,text_rect)

        text = font.render("e    end inflation, switch to radiation",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10),top=int(uniHeight/4)+200)
        screen.blit(text,text_rect)

        text = font.render("g    GODMODE, become omnipotent",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10),top=int(uniHeight/4)+250)
        screen.blit(text,text_rect)

        text = font.render("r    reset simulation",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10),top=int(uniHeight/4)+300)
        screen.blit(text,text_rect)

        text = font.render("m    THE SOUND OF SILENCE",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10),top=int(uniHeight/4)+350)
        screen.blit(text,text_rect)

        text = font.render("SPACE    START/PAUSE",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10)-30,top=int(uniHeight/4)+400)
        screen.blit(text,text_rect)

        text = font.render("ENTER    speed up time 10x",True,WHITE)
        text_rect = text.get_rect(left=int(uniWidth/10)-30,top=int(uniHeight/4)+450)
        screen.blit(text,text_rect)

        pausex += 2 

        pygame.display.flip()
        clock.tick(maxfps)
