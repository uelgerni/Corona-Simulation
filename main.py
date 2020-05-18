
from SocialDistancing import *

# testing parameters for sim get imported since they are needed in BasicSim anyways


def SocialDistancing():
    # testing populations and areas
    population2 = initializeSD(n, iPerc, sPerc, xlowerlimit=500, xLimit=1000, ylowerlimit=0, yLimit=yLim,
                               SDPercentage=0)
    population = initializeSD(n, iPerc, sPerc, xlowerlimit=0, xLimit=xLim / 2, ylowerlimit=ylowerlim, yLimit=yLim,
                              SDPercentage=100)
    poplist = (population, population2)
    # allowedareas = [Area(xlowerlim, xLim, ylowerlim, yLim), Area(0, xLim, 0, yLim)]
    simulation(poplist)


def basicSim():
    # sim
    population2 = initialize(n, iPerc, sPerc, xlowerlimit=500, xLimit=1000, ylowerlimit=0, yLimit=yLim)
    population = initialize(n, iPerc, sPerc, xlowerlimit=0, xLimit=xLim / 2, ylowerlimit=ylowerlim, yLimit=yLim)
    poplist = (population, population2)
    # allowedareas = [Area(xlowerlim, xLim, ylowerlim, yLim), Area(0, 1000, ylowerlim, yLim)]
    simulation(poplist)


# basicSim()
SocialDistancing()
