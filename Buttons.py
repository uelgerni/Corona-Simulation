# -*- coding: utf-8 -*-
"""
Created on Tue May 19 10:18:54 2020

@author: Suri
"""

from SocialDistancing import *

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont('Arial', 20)
active = False
lockdownFlag = False





def textobjects(text, font):
    textsurface = font.render(text, True, (0, 0, 0))
    return textsurface, textsurface.get_rect()


def button(x, y, label, length, height, standard_colour, active_colour, border):
    global active
    global lockdownFlag
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + length and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_colour, (x, y, length, height))
        if click[0] == 1 and not active:
            active = True
            if label == "Standard Simulation":
                population1 = initialize(popSize=popsize1, infectedPercentage=iPerc, sickPercentage=sPerc,
                                         xlowerlimit=xlowerlim,
                                         xLimit=xLim, ylowerlimit=0, yLimit=yLim)
                population2 = initializeSD(popSize=popsize2, infectedPercentage=iPerc, sickPercentage=sPerc,
                                           xlowerlimit=0,
                                           xLimit=xlowerlim, ylowerlimit=0, yLimit=yLim,
                                           SDPercentage=0)
                population = population1.append(population2, ignore_index=True)
                simulation(population, lockdownFlag)


            elif label == 'Social Distancing 20%':
                population1 = initialize(popSize=popsize1, infectedPercentage=iPerc, sickPercentage=sPerc,
                                         xlowerlimit=xlowerlim,
                                         xLimit=xLim, ylowerlimit=0, yLimit=yLim)
                population2 = initializeSD(popSize=popsize2, infectedPercentage=iPerc, sickPercentage=sPerc,
                                           xlowerlimit=0,
                                           xLimit=xlowerlim, ylowerlimit=0, yLimit=yLim,
                                           SDPercentage=20)
                population = population1.append(population2, ignore_index=True)
                simulation(population, lockdownFlag)



            elif label == 'Social Distancing 40%':
                population1 = initialize(popSize=popsize1, infectedPercentage=iPerc, sickPercentage=sPerc,
                                         xlowerlimit=xlowerlim,
                                         xLimit=xLim, ylowerlimit=0, yLimit=yLim)
                population2 = initializeSD(popSize=popsize2, infectedPercentage=iPerc, sickPercentage=sPerc,
                                           xlowerlimit=0,
                                           xLimit=xlowerlim, ylowerlimit=0, yLimit=yLim,
                                           SDPercentage=40)
                population = population1.append(population2, ignore_index=True)
                simulation(population, lockdownFlag)



            elif label == "Exit":
                # run = False
                pygame.quit()
            elif label == "Lockdown":
                lockdownFlag = True
        if click[0] == 0:
            active = False
    else:
        pygame.draw.rect(screen, standard_colour, (x, y, length, height))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, length, height), border)
    textground, textbox = textobjects(label, font)
    textbox.center = (int(np.floor((x + (length / 2)))), int(np.floor(y + (height / 2))))
    screen.blit(textground, textbox)



