from SocialDistancing import *

# some testing parameters for sim get imported since they are needed in BasicSim anyways
iPerc = 1  # percentage infected with no symptoms start
sPerc = .5  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
lockdownFlag = True


def SocialDistancing():
    # testing populations and areas
    population1 = initializeSD(popSize=100, infectedPercentage=iPerc, sickPercentage=sPerc, xlowerlimit=500,
                               xLimit=1000, ylowerlimit=0, yLimit=yLim,
                               SDPercentage=100)
    population2 = initializeSD(popSize=100, infectedPercentage=iPerc, sickPercentage=sPerc, xlowerlimit=0,
                               xLimit=500, ylowerlimit=0, yLimit=yLim,
                               SDPercentage=0)
    population = population1.append(population2, ignore_index=True)
    simulation(population, lockdownFlag)


def basicSim():
    # sim
    population1 = initialize(popSize=100, infectedPercentage=iPerc, sickPercentage=sPerc, xlowerlimit=500,
                             xLimit=1000, ylowerlimit=0, yLimit=yLim)
    population2 = initialize(popSize=100, infectedPercentage=iPerc, sickPercentage=sPerc, xlowerlimit=0,
                             xLimit=500, ylowerlimit=0, yLimit=yLim)
    population = population1.append(population2, ignore_index=True)
    simulation(population, lockdownFlag)


basicSim()
SocialDistancing()
