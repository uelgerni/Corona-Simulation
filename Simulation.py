from Person import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as anim
import pandas as pd
import time

# testing parameters for sim
n = 500
iPerc = 5  # percentage infected with no symptoms start
sPerc = 5  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
xLim, yLim = 1000, 1000  # area size
contagionDist = 15  # distance where spread is possible
contagionP = 25  # chance to spread when in reach
infectedArray = np.array(0)
criticalArray = np.array(0)
healthyArray = np.array(n)
deadArray = np.array(0)
dayArray = np.array(0)
recoveredArray = np.array(0)


def initialize(popSize, infectedPercentage, sickPercentage, xLimit, yLimit):
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
    initInfectedNum = int(np.floor(popSize * infectedPercentage / 100))
    initSickNum = int(np.floor(popSize * sickPercentage / 100))
    initialInfected = population.sample(n=initInfectedNum).index.values.tolist()
    initialSick = population.sample(n=initSickNum).index.values.tolist()

    # infecting those unlucky people
    for index in initialInfected:
        population.at[index, 'Person'].setInfected()
        population.at[index, 'Health'] = Health.INFECTED
    for index in initialSick:
        population.at[index, 'Person'].setSick()
        population.at[index, 'Health'] = Health.SICK
    return population


def updatePop(pop: pd.DataFrame):
    for person in pop['Person']:
        if not person.infectious:
            pass
        else:
            pop['Person'].apply(lambda z: z.setInfected() if checkForInfect(z) else z)
    pop['Person'].apply(Person.update)
    pop['xCoord'], pop['yCoord'] = \
        pop['Person'].apply(lambda z: z.currentLocation.x), pop['Person'].apply(lambda z: z.currentLocation.y)

    numInfected = pop['Person'].apply(lambda z: 1 if z.infectious else 0).sum()
    numCritical = pop['Person'].apply(lambda z: 1 if z.health is Health.CRITICAL else 0).sum()
    numDead = pop['Person'].apply(lambda z: 1 if z.health is Health.DEAD else 0).sum()
    numHealthy = len(pop.index) - numInfected - numDead
    numRecovered = pop['Person'].apply(lambda z: 1 if z.health is Health.RECOVERED else 0).sum()
    return numHealthy, numInfected, numCritical, numDead, numRecovered


def checkForInfect(z):
    if z.currentLocation.getDistanceLoc(z.currentLocation) < contagionDist:
        if not z.immune:
            if random.random() < contagionP / 100:
                return True
    return False


population = initialize(n, iPerc, sPerc, xLim, yLim)
# plotting stuff

# making a color list corresponding to health status
colors = [x.getColor() for x in population['Person']]

# creating the plot


from matplotlib.lines import Line2D

# making custom a custom legend
custom_lines = [Line2D([0], [0], color='w', markerfacecolor='green', lw=6, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='yellow', lw=6, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='orange', lw=6, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='red', lw=4, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='blue', lw=4, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='gray', lw=4, marker='o')]

for i in range(1000):

    stats = updatePop(population)
    colors = [x.getColor() for x in population['Person']]

    #auskommentiert für niklas
   # population.plot(x='xCoord', y='yCoord', kind='scatter', c=colors)
   # plt.axis([0, 1000, 0, 1000])
   # plt.figlegend(custom_lines, ['Healthy', 'Infected', 'Sick', 'Hospitalized', 'Recovered', 'Dead'])
   # plt.savefig("simFigs/" + "{:03}".format(i))
   # plt.close()

    healthyArray = np.append(healthyArray, stats[0])
    infectedArray = np.append(infectedArray, stats[1])
    criticalArray = np.append(criticalArray, stats[2])
    deadArray = np.append(deadArray, stats[3])
    dayArray = np.append(dayArray, i + 1)
    recoveredArray = np.append(recoveredArray, stats[4])

    plt.plot(dayArray, healthyArray, color='green')
    plt.plot(dayArray, deadArray, color='grey')
    plt.plot(dayArray, infectedArray, color='yellow')
    plt.plot(dayArray, criticalArray, color='red')
    plt.plot(dayArray, recoveredArray, color='blue')

    plt.axis([0, 100, 0, 550])
    plt.figlegend(custom_lines, ['Healthy', 'Infected', 'Sick', 'Hospitalized', 'Recovered', 'Dead'])

    plt.savefig("simStats/" + "{:03}".format(i))

    plt.close()
