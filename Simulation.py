from Person import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as anim
import pandas as pd
import time

# testing parameters for sim
n = 500
iPerc = 4  # percentage infected with no symptoms start
sPerc = 2  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
xLim, yLim = 1000, 1000  # area size
contagionDist = 10  # distance where spread is possible
contagionP = 15  # chance to spread when in reach

infectedNum = 0
healthyNum = n
recoveredNum = 0
criticalNum = 0


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


population = initialize(n, iPerc, sPerc, xLim, yLim)


def updatePop(pop: pd.DataFrame):
    for person in pop['Person']:
        if not person.infectious:
            pass
        else:
            pop['Person'].apply(lambda z: z.setInfected() if (
                    z.currentLocation.getDistanceLoc(
                        z.currentLocation) < contagionDist & z.immune is False & random.random() < contagionP / 100) else z)
    pop['Person'].apply(Person.update)
    pop['xCoord'], pop['yCoord'] = \
        pop['Person'].apply(lambda z: z.currentLocation.x), pop['Person'].apply(lambda z: z.currentLocation.y)
    numInfected = pop['Person'].apply(lambda z: 1 if z.infectious else 0).sum()
    numCritical = pop['Person'].apply(lambda z: 1 if z.health is Health.CRITICAL else 0).sum()
    numHealthy = pop.size - numInfected

    return numInfected, numCritical, numHealthy


# plotting stuff

# making a color list corresponding to health status
colors = [x.getColor() for x in population['Person']]

# creating the plot

fig, axs = plt.subplots(2)
from matplotlib.lines import Line2D

# making custom a custom legend
custom_lines = [Line2D([0], [0], color='w', markerfacecolor='green', lw=6, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='yellow', lw=6, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='orange', lw=6, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='red', lw=4, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='blue', lw=4, marker='o'),
                Line2D([0], [0], color='w', markerfacecolor='gray', lw=4, marker='o')]

population.plot(x='xCoord', y='yCoord', kind='scatter', c=colors)
plt.legend(custom_lines, ['Healthy', 'Infected', 'Sick', 'Hospitalized', 'Recovered', 'Dead'])
plt.close()

for i in range(1000):
    updatePop(population)
    colors = [x.getColor() for x in population['Person']]
    population.plot(x='xCoord', y='yCoord', kind='scatter', c=colors)
    plt.axis([0, 1000, 0, 1000])
    plt.figlegend(custom_lines, ['Healthy', 'Infected', 'Sick', 'Hospitalized', 'Recovered', 'Dead'])
    plt.savefig("simFigs/" + "{:03}".format(i))
    plt.close()
