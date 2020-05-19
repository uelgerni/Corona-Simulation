import pygame
from sys import exit
from Person import *
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation as anim
import pandas as pd
import time
import numpy as np

# normal scenario, no social distancing or borders
# testing parameters for all sims


contagionDist = 10  # distance where spread is possible
contagionP = 100  # chance to spread when in reach
iPerc = 2  # percentage infected with no symptoms start
sPerc = 1  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
lockdownFlag = False
popsize1 = 75
popsize2 = 75


def initialize(popSize, infectedPercentage, sickPercentage, xlowerlimit, xLimit, ylowerlimit, yLimit):
    area = Area(xlowerlimit=xlowerlimit, xlimit=xLimit, ylowerlimit=ylowerlimit, ylimit=yLimit)  # testarea
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
    # infecting
    for person in pop['Person']:
        if not person.infectious:
            pass
        else:
            pop['Person'].apply(lambda z: z.setInfected() if checkForInfect(z, person) else z)
    # updating dataframe
    pop['Person'].apply(lambda z: z.update(lockdownFlag))
    pop['xCoord'], pop['yCoord'] = \
        pop['Person'].apply(lambda z: z.currentLocation.x), pop['Person'].apply(lambda z: z.currentLocation.y)

    # statistics
    numInfected = pop['Person'].apply(lambda z: 1 if z.infectious else 0).sum()
    numCritical = pop['Person'].apply(lambda z: 1 if z.health is Health.CRITICAL else 0).sum()
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
    FPS = 144  # frames per second setting
    fpsClock = pygame.time.Clock()
    win = pygame.display.set_mode((xLim, yLim + 215))  # more space in y direction for stats and legend

    # caption
    pygame.display.set_caption("Corona Simulation")
    run = True

    # initializing our stat arrays, 0 is at top, so 200 is our "new zero"
    infections, critical = np.array([200]), np.array([200])

    while run:
        pygame.time.delay(0)
        # if escape is pressed or the X button on the top right it closes the window and ends the simulation
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.QUIT:
                run = False

        # updatePop updates pop and returns health data
        data = updatePop(population, lockdownFlag)

        # save the data
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


def draw(population, win, stats, lockdownFlag):
    for i in range(len(population)):
        x = int(np.floor(population.at[i, 'Person'].currentLocation.x))
        y = int(np.floor(population.at[i, 'Person'].currentLocation.y))
        color = population.at[i, 'Person'].getColor()

        # draw the pop
        pygame.draw.circle(win, color, (x, y + 205), 10)

        # border between areas, thick if lockdownFlag
        width = 3 if lockdownFlag else 1

        pygame.draw.line(win, pygame.Color(0, 0, 0), (xlowerlim, 203), (xlowerlim, yLim + 215), width)
        pygame.draw.line(win, pygame.Color(0, 0, 0), (0, 203), (xLim, 203))

        # drawing stats above sim
        pygame.draw.lines(win, (255, 215, 0), False, stats[0], 3)  # infections surface, color, closed, data, width
        pygame.draw.lines(win, (255, 0, 0), False, stats[1], 3)  # critical

      