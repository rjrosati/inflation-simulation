#! /usr/bin/env python3
import math
import sys
import pygame
import numpy as np
import random
import os

if getattr(sys, "frozen", False):
    basepath = os.path.dirname(sys.executable)
else:
    basepath = os.path.dirname(os.path.abspath(__file__))

fontpath = os.path.join(basepath, "PressStart2P.ttf")
if not os.path.exists(fontpath):
    print("Error: font file not found. I looked in " + fontpath)
    sys.exit(-1)
musicpath = os.path.join(basepath, "keygen_music.mp3")
if not os.path.exists(musicpath):
    print("Error: music file not found. I looked in " + musicpath)
    sys.exit(-1)
laserpath = os.path.join(basepath, "laser.aiff")
if not os.path.exists(laserpath):
    print("Error: laser sound effect file not found. I looked in " + laserpath)
    sys.exit(-1)
rs = []

uniWidth = 900
uniHeight = 900
blk = 100
pygame.init()
screen = pygame.display.set_mode((uniWidth, uniHeight), pygame.SHOWN)
clock = pygame.time.Clock()
maxfps = 60
font = pygame.font.Font(fontpath, 20)
bigfont = pygame.font.Font(fontpath, 30)
dt = 0.01
dti_per_frame = dt_per_frame = 1
circle_width = 2
c = 10
num_dt = 0
pulse_t = 4
t = 0
a0 = 1
pausex = 0
WHITE     = (255, 255, 255)
RED       = (255, 0, 0)
GREEN     = (0,   255, 0)
BLUE      = (0,   0, 255)
YELLOW    = (255, 255, 0)
CYAN      = (0,   255, 255)
MAGENTA   = (255, 0, 255)
BLACK     = (0,   0, 0)
DARKBLUE  = (61,  116, 181)
DARKRED   = (175, 69, 79)
DARKGREEN = (103, 131, 93)
q = 1
FASTFACTOR = 5

colors = [WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, BLACK]
bkcolors = [DARKRED, DARKGREEN, DARKBLUE, BLACK]

H0 = 1e-4
# in general, goes like a**(-3*(w+1))
# also, epsilon is 3/2(1+w), or __ w = 2e/3 - 1 __
def const_w_EOS(a,w):
    return a**(-3*(w+1))

def recompute_grid(t, center_x, center_y, a1):
    # create a square grid, comoving
    grid = []
    w, h, b = uniWidth, uniHeight, blk
    ws, hs = 0, 0
    # rescale grid when no longer visible
    while a1 > w / b:
        a1 /= w / b
    for x in range(ws, w, b):
        for y in range(hs, h, b):
            grid.append(
                pygame.Rect(
                    a1 * (x - center_x) + center_x,
                    a1 * (y - center_y) + center_y,
                    a1 * b,
                    a1 * b,
                )
            )
    return grid


def recompute_check(t, center_x, center_y, a1):
    # create a square grid, comoving
    grid = []
    w, h, b = uniWidth, uniHeight, blk
    ws, hs = 0, 0
    # don't rescale grid when no longer visible
    for x in range(ws, w, b):
        for y in range(hs, h, b):
            grid.append(
                pygame.Rect(
                    a1 * (x - center_x) + center_x,
                    a1 * (y - center_y) + center_y,
                    a1 * b,
                    a1 * b,
                )
            )
    return grid


def blit_txt_with_outline(screen, loc, font, text, fg_color, bg_color, thk):
    textfg = font.render(text, True, fg_color)
    textbg = font.render(text, True, bg_color)
    screen.blit(textbg, loc + (-thk, -thk))
    screen.blit(textbg, loc + (thk, -thk))
    screen.blit(textbg, loc + (-thk, thk))
    screen.blit(textbg, loc + (thk, thk))
    screen.blit(textbg, loc + (0, -thk))
    screen.blit(textbg, loc + (0, thk))
    screen.blit(textbg, loc + (-thk, 0))
    screen.blit(textbg, loc + (thk, 0))
    screen.blit(textfg, loc)
    return


drawing_plot = True
p_shape = np.array((400, 200), dtype=int)
p_loc = np.array((uniWidth - (p_shape[0] + 50), 50), dtype=int)
xlim = np.array((0, 200), dtype=int)
ylim = np.array((0, 500), dtype=int)
points = []
dpoints = []
godpoints = []
goddpoints = []
ticksize = 10
axiscolor = CYAN
plotcolor = RED
dplotcolor = WHITE
ylabel = "c.h."
xlabel = "t"


def draw_plot(screen):
    # draw background
    pygame.draw.rect(screen, BLACK, (p_loc[0], p_loc[1], p_shape[0], p_shape[1]))
    # x axis and ticks
    pygame.draw.line(
        screen,
        axiscolor,
        (p_loc[0], p_loc[1] + p_shape[1]),
        (p_loc[0] + p_shape[0], p_loc[1] + p_shape[1]),
        3,
    )
    for x in range(p_loc[0], p_shape[0] + p_loc[0], 40):
        pygame.draw.line(
            screen,
            axiscolor,
            (x, p_loc[1] + p_shape[1]),
            (x, p_loc[1] + p_shape[1] - ticksize),
        )
    # y axis and ticks
    pygame.draw.line(
        screen, axiscolor, (p_loc[0], p_loc[1]), (p_loc[0], p_loc[1] + p_shape[1]), 3
    )
    for y in range(p_loc[1], p_shape[1] + p_loc[1], 40):
        pygame.draw.line(screen, axiscolor, (p_loc[0], y), (p_loc[0] + ticksize, y))
    # axis labels
    text = font.render(xlabel, True, WHITE, BLACK)
    screen.blit(text, p_loc + p_shape + (-3 * ticksize, -3 * ticksize))
    text = font.render(ylabel, True, WHITE, BLACK)
    screen.blit(text, p_loc + (3 * ticksize, 2 * ticksize))

    # curve
    p = godpoints if godmode else points
    d = goddpoints if godmode else dpoints
    if len(p) > 1:
        pygame.draw.lines(screen, plotcolor, False, p, 3)
        if (p[-1][0] > p_loc[0] + p_shape[0]) or (p[-1][1] < p_loc[1]):
            pygame.draw.rect(screen, BLACK, (230, 830, 610, 50))
            blit_txt_with_outline(
                screen,
                (250, 850),
                font,
                "INFLATION IS OFF THE CHARTS!!",
                WHITE,
                BLACK,
                10,
            )

    if len(d) > 1:
        pygame.draw.lines(screen, dplotcolor, False, d, 3)

    return


done = False
paused = True
godmode = False
light_traveling = False
lights_traveling = False
horizons = False
music = False
fast = False
slow = False
godgrid = recompute_grid(t, uniWidth / 2, uniHeight / 2, 1)
godcheck = recompute_check(t, uniWidth / 2, uniHeight / 2, 1)
checkcolors = [random.choice(bkcolors) for i in range(len(godcheck))]
at = []
a = a0
H = H0
eh = 0
tswitch = np.inf
inflating = True
pygame.mixer.init()
pygame.mixer.music.load(musicpath)
pygame.mixer.music.play(loops=-1)
pewpew = pygame.mixer.Sound(laserpath)
music = True
while not done:
    keys = pygame.key.get_pressed()
    fast = keys[pygame.K_RETURN]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if light_traveling:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos2 = pygame.mouse.get_pos()
                pos2 = (pos2 - np.array((uniWidth / 2, uniHeight / 2))) / (
                    a / q
                ) + np.array((uniWidth / 2, uniHeight / 2))
                lights_traveling = True
                distance = np.linalg.norm((pos1 - pos2))
                tc = t
                td = t + 1000
                rs = [0]
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos1 = pygame.mouse.get_pos()
                pos1 = (pos1 - np.array((uniWidth / 2, uniHeight / 2))) / (
                    a / q
                ) + np.array((uniWidth / 2, uniHeight / 2))
                light_traveling = True
                tc = t
                td = t + 1000
                rs = [0]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = True
            if event.key == pygame.K_p:
                drawing_plot = not drawing_plot
            if event.key == pygame.K_SPACE:
                paused = not paused
                if not paused:
                    pewpew.play()
            if event.key == pygame.K_g:
                godmode = not godmode
            if event.key == pygame.K_n:
                slow = not slow
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                if not music:
                    pygame.mixer.init()
                    pygame.mixer.music.load(musicpath)
                    pygame.mixer.music.play(loops=-1)
                    music = True
                else:
                    pygame.mixer.music.stop()
                    music = False
            if event.key == pygame.K_h:
                horizons = not horizons
            if event.key == pygame.K_e and inflating:
                # let's end inflation, switch a(t) to a different function
                # TODO instead, we should solve this as an ode. but how if we don't know tswitch?? hmmm
                # probably just make the transition fast, use a(t,tswitch=inf) until keypress, then jump to a(t,tswitch=tkeypress+3s)
                # where we choose the time to minimize the discontinuity
                inflating = False
                tswitch = t
                #a = lambda t: infla(tswitch) + rad(t - tswitch)
                #H = lambda t: radH(t)
                #e = lambda tc, t, godmode: min(
                #    10000, np.exp(t - tswitch) * event_horizon(tc, tswitch, godmode)
                #)
                # horizons = False
            if event.key == pygame.K_r:
                # reset to the beginning
                inflating = True
                light_traveling = False
                lights_traveling = False
                horizons = True
                num_dt = 0
                eh = 0
                a = a0
                H = H0
                tswitch = np.inf
                points = []
                godpoints = []
                goddpoints = []
                dpoints = []
                at = []

    if not paused:
        if fast:
            dt_per_frame = dti_per_frame * FASTFACTOR
        else:
            dt_per_frame = dti_per_frame
        num_dt += 1

        t = num_dt * dt
        OmegaR=0
        OmegaL=1
        eps = 3.0*np.tanh(t-(tswitch+3.0))/2.0
        H = H0 * np.sqrt(OmegaR*const_w_EOS(a,1./3.) + OmegaL*const_w_EOS(a,2*eps/3-1))
        da = H*a*dti_per_frame
        a += da
        
        # event horizon
        # d_event_horizon = a(t)* int_0^t0 c/a(t) dt
        deh = c / a * dti_per_frame
        eh += deh

        if fast:
            for _ in range(FASTFACTOR-1):
                H = H0 * np.sqrt(OmegaR*const_w_EOS(a,1./3.) + OmegaL*const_w_EOS(a,2*eps/3-1))
                da = H*a*dti_per_frame
                a += da

                deh = c / a * dti_per_frame
                eh += deh
        at.append(a)
        
        points.append(
            p_loc
            + (0, +p_shape[1])
            + (t / xlim[1] * p_shape[0], -eh / ylim[1] * p_shape[1])
        )
        godpoints.append(
            p_loc
            + (0, +p_shape[1])
            + (t / xlim[1] * p_shape[0], -a*eh / ylim[1] * p_shape[1])
        )

        if lights_traveling:
            dpoints.append(
                p_loc
                + (0, +p_shape[1])
                + (t / xlim[1] * p_shape[0], -distance * a / ylim[1] * p_shape[1])
            )
            goddpoints.append(
                p_loc
                + (0, +p_shape[1])
                + (t / xlim[1] * p_shape[0], -distance / ylim[1] * p_shape[1])
            )

        if light_traveling:
            if tc <= t <= td:
                if np.allclose((t - tc) % pulse_t, 0):
                    rs.append(0)
                for i in range(len(rs)):
                    v = c + H * rs[i]
                    rs[i] += v * dt
            else:
                tc = t
                td = t + 100
                rs = [0]
                # light_traveling = False

        if num_dt % dt_per_frame == 0:
            screen.fill(BLACK)
            if godmode:
                q = a
                grid = godgrid
                check = godcheck
            else:
                q = 1
                grid = recompute_grid(t, uniWidth / 2, uniHeight / 2, a)
                check = recompute_check(t, uniWidth / 2, uniHeight / 2, a)

            for square, color in zip(check, checkcolors):
                pygame.draw.rect(screen, color, square)

            if light_traveling:
                pos1_tmp = (
                    np.array((uniWidth / 2, uniHeight / 2))
                    + (pos1 - np.array((uniWidth / 2, uniHeight / 2))) * a / q
                )
                for r in rs:
                    pygame.draw.circle(
                        screen,
                        YELLOW,
                        (int(pos1_tmp[0]), int(pos1_tmp[1])),
                        int(r / q),
                        0 if int(r / q) < 5 else circle_width,
                    )
                if horizons:
                    h = e(tc, t, godmode)
                    pygame.draw.circle(
                        screen,
                        RED,
                        (int(pos1_tmp[0]), int(pos1_tmp[1])),
                        int(h),
                        0 if int(h) < 5 else circle_width,
                    )
                if lights_traveling:
                    pos2_tmp = (
                        np.array((uniWidth / 2, uniHeight / 2))
                        + (pos2 - np.array((uniWidth / 2, uniHeight / 2))) * a / q
                    )
                    for r in rs:
                        pygame.draw.circle(
                            screen,
                            YELLOW,
                            (int(pos2_tmp[0]), int(pos2_tmp[1])),
                            int(r / q),
                            0 if int(r / q) < 5 else circle_width,
                        )
                    distance = np.linalg.norm((pos1 - pos2))
                    if horizons:
                        h = e(tc, t, godmode)
                        pygame.draw.circle(
                            screen,
                            RED,
                            (int(pos2_tmp[0]), int(pos2_tmp[1])),
                            int(h),
                            0 if int(h) < 5 else circle_width,
                        )

            blit_txt_with_outline(
                screen, (20, 20), font, "t = %6.4f" % t, WHITE, BLACK, 10
            )
            blit_txt_with_outline(
                screen, (20, 50), font, "a(t) = %3.2f" % a, WHITE, BLACK, 10
            )

            if drawing_plot:
                draw_plot(screen)

            pygame.display.flip()
            clock.tick(maxfps)
    else:
        # show instructions
        screen.fill(BLACK)
        fun_color = random.choice(colors)
        wletters = "...o0o0o TEAM LHS=RHS o0o0o..."
        i = 0
        for letter in wletters:
            y = 120 + 30 * np.sin(2 * np.pi / (uniWidth / 2) * (pausex + i * 30))
            x = pausex + i * 30
            x %= uniWidth
            i += 1
            text = bigfont.render(letter, True, fun_color)
            screen.blit(text, (x, y))

        text = bigfont.render("INFLATION SIMULATOR 9000", True, fun_color)
        text_rect = text.get_rect(center=(int(uniWidth / 2), 50))
        screen.blit(text, text_rect)

        text = font.render("SPACE    START/PAUSE", True, WHITE)
        text_rect = text.get_rect(
            left=int(uniWidth / 10) - 80, top=int(uniHeight / 4) + 50
        )
        screen.blit(text, text_rect)

        text = font.render("ENTER    speed up time 10x", True, WHITE)
        text_rect = text.get_rect(
            left=int(uniWidth / 10) - 80, top=int(uniHeight / 4) + 100
        )
        screen.blit(text, text_rect)

        text = font.render("CLICK    release light beam", True, WHITE)
        text_rect = text.get_rect(
            left=int(uniWidth / 10) - 80, top=int(uniHeight / 4) + 150
        )
        screen.blit(text, text_rect)

        text = font.render("p    display a(t) plot", True, WHITE)
        text_rect = text.get_rect(left=int(uniWidth / 10), top=int(uniHeight / 4) + 200)
        screen.blit(text, text_rect)

        text = font.render("h    display event horizon", True, WHITE)
        text_rect = text.get_rect(left=int(uniWidth / 10), top=int(uniHeight / 4) + 250)
        screen.blit(text, text_rect)

        text = font.render("e    end inflation, switch to radiation", True, WHITE)
        text_rect = text.get_rect(left=int(uniWidth / 10), top=int(uniHeight / 4) + 300)
        screen.blit(text, text_rect)

        text = font.render("g    GODMODE, become omniscient", True, WHITE)
        text_rect = text.get_rect(left=int(uniWidth / 10), top=int(uniHeight / 4) + 350)
        screen.blit(text, text_rect)

        text = font.render("r    reset simulation", True, WHITE)
        text_rect = text.get_rect(left=int(uniWidth / 10), top=int(uniHeight / 4) + 400)
        screen.blit(text, text_rect)

        text = font.render("m    THE SOUND OF SILENCE", True, WHITE)
        text_rect = text.get_rect(left=int(uniWidth / 10), top=int(uniHeight / 4) + 450)
        screen.blit(text, text_rect)

        pausex += 2

        pygame.display.flip()
        clock.tick(maxfps)
