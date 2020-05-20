import pygame
from sys import exit
from Person import *
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation as anim
import pandas as pd
import time
import numpy as np
from coronatest import *
from Params import *
"""
This is the basic simulation
In here are the methods to initialize a population, update that population for each tick, the simulation method, which
controls the ticks
"""
coronatest = Coronatest(testcap,testper)

def initialize(popSize, infectedPercentage, sickPercentage, xlowerlimit, xLimit, ylowerlimit, yLimit, name="name"):
    area = Area(xlowerlimit=xlowerlimit, xlimit=xLimit, ylowerlimit=ylowerlimit, ylimit=yLimit, name=name)  # testarea
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

    # infecting those unlucky people
    for index in initialInfected:
        population.at[index, 'Person'].setInfected()
        population.at[index, 'Health'] = Health.INFECTED
    for index in initialSick:
        population.at[index, 'Person'].setSick()
        population.at[index, 'Health'] = Health.SICK
    return population


def updatePop(pop: pd.DataFrame, lockdownFlag):
    coronatest.update()
    # infecting and testing
    for person in pop['Person']:
        if not person.infectious:
            pass
        else:
            pop['Person'].apply(lambda z: z.setInfected() if checkForInfect(z, person) else z)
        if coronatest.persontest(person.health) is Testresult.INFECTED:
            person.testpos = True


    # updating dataframe
    pop['Person'].apply(lambda z: z.update(lockdownFlag))
    pop['xCoord'], pop['yCoord'] = \
        pop['Person'].apply(lambda z: z.currentLocation.x), pop['Person'].apply(lambda z: z.currentLocation.y)

    # statistics
    numInfected = pop['Person'].apply(lambda z: 1 if z.infectious else 0).sum()
    numCritical = pop['Person'].apply(lambda z: 1 if z.health is Health.CRITICAL else 0).sum()
    # just if you want more data, currently not used
    # numDead = pop['Person'].apply(lambda z: 1 if z.health is Health.DEAD else 0).sum()
    # numHealthy = len(pop.index) - numInfected - numDead
    # numRecovered = pop['Person'].apply(lambda z: 1 if z.health is Health.RECOVERED else 0).sum()
    return numInfected, numCritical


def checkForInfect(z, person):
    if z.currentLocation.getDistanceLoc(person.currentLocation) < contagionDist:
        if not z.immune:
            if random.random() < contagionP / 100:
                return True
    return False


def simulation(population, lockdownFlag):
    # initializing pygame
    pygame.init()

    # frame settings and window init
    FPS = 60  # frames per second setting
    fpsClock = pygame.time.Clock()
    win = pygame.display.set_mode((xLim + 10, yLim + 220))  # more space in y direction for stats and legend

    # caption
    pygame.display.set_caption("Corona Simulation")

    # initializing our stat arrays, 0 is at top, so 200 is our "new zero"
    infections, critical = np.array([200]), np.array([200])

    while True:
        pygame.time.delay(0)
        # if escape is pressed or the X button on the top right it closes the window and ends the simulation
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit("pressed escape to exit")
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit("eventtype pygame.QUIT")

        # updatePop updates pop and returns health data
        data = updatePop(population, lockdownFlag)

        # save the data, 200 offset and - because (0,0) is top left
        infections = np.append(infections, 200 - data[0])
        critical = np.append(critical, 200 - data[1])

        # for our x axis
        n = len(infections)
        x_values = np.arange(n) + 1

        # list of 2 lists of tuples, for less crowded method signatures
        infectionStat, critStat = np.array(list(zip(x_values, infections))), np.array(list(zip(x_values, critical)))
        stats = (infectionStat, critStat)

        # white background
        win.fill((255, 255, 255))
        draw(population, win, stats, lockdownFlag)

        # update our display and clock
        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()
    exit()


"""
The plotting function
"""


def draw(population, win, stats, lockdownFlag):
    # our legend
    font = pygame.font.SysFont('Comic Sans MS', 30)
    healthyText = font.render('Healthy', True, (0, 255, 0))
    infectedText = font.render('Infected', True, (255, 215, 0))
    sickText = font.render('Sick', True, (255, 135, 0))
    criticalText = font.render('Critical', True, (255, 0, 0))
    deadText = font.render('Recovered', True, (0, 0, 255))
    recoveredText = font.render('Dead', True, (0, 0, 0))

    # plot the population
    for i in range(len(population)):
        x = int(np.floor(population.at[i, 'Person'].currentLocation.x))
        y = int(np.floor(population.at[i, 'Person'].currentLocation.y))
        color = population.at[i, 'Person'].getColor()

        # draw the pop
        pygame.draw.circle(win, color, (x + 5, y + 208), 10)

    # border between areas, thick if lockdownFlag.
    width = 3 if lockdownFlag else 1
    pygame.draw.line(win, pygame.Color(0, 0, 0), (xlowerlim + 3, 205), (xlowerlim + 3, yLim + 215), width)
    # borders around it all. All the +5's are for borders near edges
    pygame.draw.line(win, pygame.Color(0, 0, 0), (5, 205), (xLim + 5, 205), 3)  # top
    pygame.draw.line(win, pygame.Color(0, 0, 0), (5, yLim + 215), (xLim + 5, yLim + 215), 3)  # bottom
    pygame.draw.line(win, pygame.Color(0, 0, 0), (5, 205), (5, yLim + 215), 3)  # left
    pygame.draw.line(win, pygame.Color(0, 0, 0), (xLim + 5, 205), (xLim + 5, yLim + 215), 3)  # right

    # drawing stats above sim
    pygame.draw.lines(win, (255, 215, 0), False, stats[0], 3)  # infections surface, color, closed, data, width
    pygame.draw.lines(win, (255, 0, 0), False, stats[1], 3)  # critical

    # blitting the legend onto our main window
    win.blit(healthyText, (0, 0))
    win.blit(infectedText, (0, 20))
    win.blit(sickText, (0, 40))
    win.blit(criticalText, (0, 60))
    win.blit(deadText, (0, 80))
    win.blit(recoveredText, (0, 100))