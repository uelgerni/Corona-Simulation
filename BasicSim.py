import pygame
from sys import exit
from Person import *
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation as anim
import pandas as pd
import time

# normal scenario, no social distancing or borders
# testing parameters for all sims
n = 5

xlowerlim, xLim, ylowerlim, yLim = 500, 1000, 0, 800  # area size
contagionDist = 25  # distance where spread is possible
contagionP = 10  # chance to spread when in reach

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
    numDead = pop['Person'].apply(lambda z: 1 if z.health is Health.DEAD else 0).sum()
    numHealthy = len(pop.index) - numInfected - numDead
    numRecovered = pop['Person'].apply(lambda z: 1 if z.health is Health.RECOVERED else 0).sum()
    return numHealthy, numInfected, numCritical, numDead, numRecovered


def checkForInfect(z, person):
    if z.currentLocation.getDistanceLoc(person.currentLocation) < contagionDist:
        if not z.immune:
            if random.random() < contagionP / 100:
                return True
    return False


def simulation(population, lockdownFlag):
    pygame.init()
    FPS = 144  # frames per second setting
    fpsClock = pygame.time.Clock()
    win = pygame.display.set_mode((xLim, yLim))
    # This line creates a window of 1000 width, 1000 height
    pygame.display.set_caption("Corona Simulation")
    run = True

    while run:
        pygame.time.delay(0)
        # if escape is pressed or the X button on the top right it closes the window and ends the simulation
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.QUIT:
                run = False
        updatePop(population, lockdownFlag)

        # white background
        win.fill((255, 255, 255))
        draw(population, win)

        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()
    exit()


def draw(population, win):
    for i in range(len(population)):
        x = int(np.floor(population.at[i, 'Person'].currentLocation.x))
        y = int(np.floor(population.at[i, 'Person'].currentLocation.y))
        color = population.at[i, 'Person'].getColor()

        pygame.draw.circle(win, color, (x, y), 10)
        pygame.draw.line(win, pygame.Color(0, 0, 0), (500, 0), (500, 800))
