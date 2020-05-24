# -*- coding: utf-8 -*-
"""
Created on Tue May 19 10:18:54 2020

@author: Suri
"""

from SocialDistancing import *
#pygame is initiated
pygame.init()
#window is created
screen = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont('Arial', 20)

active = False
lockdownFlag = False

#textobjects are defined
def textobjects(text, font):
    #text surface is created, font is black
    textsurface = font.render(text, True, (0, 0, 0))
    #a rectangle with the size of the text is created
    return textsurface, textsurface.get_rect()


#buttons are defined, they're dependant on an x and y position,a label, a length, height, two colours and a border
def button(x, y, label, length, height, standard_colour, active_colour, border):
    global active
    global lockdownFlag
    #gives mouse position as (x,y)
    mouse = pygame.mouse.get_pos()
    #gives information about  wether the mouse is clicked or not(as tipel with three entries)
    click = pygame.mouse.get_pressed()
    #checks wether the mouse cursor is inside the button
    if x < mouse[0] < x + length and y < mouse[1] < y + height:
        #button ist actually created in a lighter colour to show that the cursor is on the button
        pygame.draw.rect(screen, active_colour, (x, y, length, height))
        #checks wether the left mouse button is pressed and the button is already active
        if click[0] == 1 and not active:
            active = True
            #buttons get different methods, dependant on their label
            if label == "Standard Simulation":
                population1 = initialize(popSize=popsize1, infectedPercentage=iPerc, sickPercentage=sPerc,
                                         xlowerlimit=xlowerlim1,
                                         xLimit=xLim1, ylowerlimit=ylowerlim1, yLimit=yLim1)
                population2 = initializeSD(popSize=popsize2, infectedPercentage=iPerc, sickPercentage=sPerc,
                                           xlowerlimit=xlowerlim2,
                                           xLimit=xLim2, ylowerlimit=ylowerlim2, yLimit=yLim2,
                                           SDPercentage=0)
                population = population1.append(population2, ignore_index=True)
                simulation(population, lockdownFlag)


            elif label == 'Social Distancing 20%':
                population1 = initialize(popSize=popsize1, infectedPercentage=iPerc, sickPercentage=sPerc,
                                         xlowerlimit=xlowerlim1,
                                         xLimit=xLim1, ylowerlimit=ylowerlim1, yLimit=yLim1)
                population2 = initializeSD(popSize=popsize2, infectedPercentage=iPerc, sickPercentage=sPerc,
                                           xlowerlimit=xlowerlim2,
                                           xLimit=xLim2, ylowerlimit=ylowerlim2, yLimit=yLim2,
                                           SDPercentage=20)
                population = population1.append(population2, ignore_index=True)
                simulation(population, lockdownFlag)



            elif label == 'Social Distancing 60%':
                population1 = initialize(popSize=popsize1, infectedPercentage=iPerc, sickPercentage=sPerc,
                                         xlowerlimit=xlowerlim1,
                                         xLimit=xLim1, ylowerlimit=ylowerlim1, yLimit=yLim1)
                population2 = initializeSD(popSize=popsize2, infectedPercentage=iPerc, sickPercentage=sPerc,
                                           xlowerlimit=xlowerlim2,
                                           xLimit=xLim2, ylowerlimit=ylowerlim2, yLimit=yLim2,
                                           SDPercentage=60)
                population = population1.append(population2, ignore_index=True)
                simulation(population, lockdownFlag)


            #exit button is initiated
            #if exit is pressed, pygame ends
            elif label == "Exit":
                # run = False
                pygame.quit()
            elif label == "Lockdown":
                lockdownFlag = True
        if click[0] == 0:
            active = False

 # if the mouse cursor is not inside the button limits, the button is drawn in a darker colour
    else:
        pygame.draw.rect(screen, standard_colour, (x, y, length, height))
    # the border that surrounds the button is created(black)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, length, height), border)
    textground, textbox = textobjects(label, font)
    textbox.center = (int(np.floor((x + (length / 2)))), int(np.floor(y + (height / 2))))
    #the text is displayed on the textsurface
    screen.blit(textground, textbox)
