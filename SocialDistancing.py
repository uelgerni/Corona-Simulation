# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:27:28 2020

@author: Suri
"""


import pygame 

            
            
from Person import *
#import matplotlib.pyplot as plt
#from matplotlib.animation import FuncAnimation as anim
import pandas as pd
import time

# testing parameters for sim
n = 100
iPerc = 0 # percentage infected with no symptoms start
sPerc = 0  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
xLim, yLim = 1000, 800  # area size
contagionDist = 3  # distance where spread is possible
contagionP = 5  # chance to spread when in reach
SDPercentage = float(input('Please enter how many percent of the population do social Distancing: '))

def initializeSD(popSize, infectedPercentage, sickPercentage, xLimit, yLimit,SDPercentage):
    area = Area(xLimit, yLimit)  # testarea
    population = pd.DataFrame(columns=('Person', 'xCoord', 'yCoord', 'Health'))
    # generating a population
    for i in range(popSize):
        loc = randomLocation(area)
        person = Person(loc)
        population.loc[i, 'Person'], population.loc[i, 'xCoord'], population.loc[i, 'yCoord'], population.loc[
        i, 'Health'] = \
            person, person.currentLocation.x, person.currentLocation.y, person.health
    
    

    # choosing the unlucky ones to get infected/sick at the start
    infectedNum = int(np.floor(popSize * infectedPercentage / 100))
    sickNum = int(np.floor(popSize * sickPercentage / 100))
    initialInfected = population.sample(n=infectedNum).index.values.tolist()
    initialSick = population.sample(n=sickNum).index.values.tolist()
    SDNum = int(np.floor(popSize * SDPercentage / 100))
    SDPeople = population.sample(n=SDNum).index.values.tolist()



    # infecting those unlucky people
    for index in initialInfected:
        population.at[index, 'Person'].setInfected()
        population.at[index, 'Health'] = Health.INFECTED
    for index in initialSick:
        population.at[index, 'Person'].setSick()
        population.at[index, 'Health'] = Health.SICK
    for index in SDPeople:
        population.at[index,'Person'].doSocialDistancing()
    return population


population = initializeSD(n, iPerc, sPerc, xLim, yLim,SDPercentage)


def updatePop(pop: pd.DataFrame):
    for person in pop['Person']:
        if not person.infectious:
            pass
        else:
            pop['Person'].apply(lambda z: z.setInfected() if checkForInfect(z) else z)
    pop['Person'].apply(Person.update)
    pop['xCoord'], pop['yCoord'] = \
        pop['Person'].apply(lambda z: z.currentLocation.x), pop['Person'].apply(lambda z: z.currentLocation.y)


def checkForInfect(z):
    if z.currentLocation.getDistanceLoc(z.currentLocation) < contagionDist:
        if not z.immune:
            if random.random() < contagionP / 100:
                return True
    return False




pygame.init()
FPS = 200 #frames per second setting
fpsClock = pygame.time.Clock()

winSD = pygame.display.set_mode((xLim, yLim))
# This line creates a window of 1000 width, 1000 height
pygame.display.set_caption("Corona Simulation")

run = True

while run:
    pygame.time.delay(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    def draw(population):
        for i in range(n):
            x = int(np.floor(population.at[i, 'Person'].currentLocation.x))
            y = int(np.floor(population.at[i, 'Person'].currentLocation.y))
            color = population.at[i,'Person'].getColor()
            
        
            pygame.draw.circle(winSD,color, (x,y),10)   
            #pygame.display.update()

    updatePop(population)
    winSD.fill((255,255,255))
    draw(population)
    
    pygame.display.update()
    #win.fill((0,0,0))
    fpsClock.tick(FPS)
        
    
pygame.quit()

