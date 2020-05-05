from Person import *
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as anim
import pandas as pd
import time

# testing parameters for sim
n = 1500
iPerc = 10  # percentage infected with no symptoms start
sPerc = 5  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
xLim, yLim = 1000, 1000  # area size
contagionDist = 3  # distance where spread is possible
contagionP = 5  # chance to spread when in reach


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


population = initialize(n, iPerc, sPerc, xLim, yLim)


def updatePop(pop: pd.DataFrame):
    pop['Person'].apply(Person.update)
    pop['xCoord'], pop['yCoord'] = \
        pop['Person'].apply(lambda z: z.currentLocation.x), pop['Person'].apply(lambda z: z.currentLocation.y)


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

population.plot(x='xCoord', y='yCoord', kind='scatter', c=colors)
plt.legend(custom_lines, ['Healthy', 'Infected', 'Sick', 'Hospitalized', 'Recovered', 'Dead'])
plt.close()

for i in range(1000):
    updatePop(population)
    colors = [x.getColor() for x in population['Person']]
    population.plot(x='xCoord', y='yCoord', kind='scatter', c=colors)
    plt.axis([0, 1000, 0, 1000])
    plt.figlegend(custom_lines, ['Healthy', 'Infected', 'Sick', 'Hospitalized', 'Recovered', 'Dead'])
    plt.savefig("simFigs/"+"{:03}".format(i))
    plt.close()
