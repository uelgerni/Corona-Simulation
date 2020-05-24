import numpy as np
import random
from Params import *


class Area:
    def __init__(self, xlimit, ylimit, xlowerlimit=0, ylowerlimit=0, name="name"):
        self.xlimit = xlimit
        self.ylimit = ylimit
        self.xlowerlimit = xlowerlimit
        self.ylowerlimit = ylowerlimit
        self.name = name

    def __str__(self):
        return "Area " + str(self.name) + " Size = (" + str(self.xlimit) + ", " + str(self.ylimit) + ")"


# simple location objects which know their area and can calculate a distance
class Location:
    def __init__(self, x, y, area: Area):
        self.x = x
        self.y = y
        self.area = area

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    # euclidean distance
    def getDistance(self, x, y):
        result = np.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return result

    def getDistanceLoc(self, other):
        result = np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        return result

    def getCopy(self):
        result = Location(self.x, self.y, self.area)
        return result


def randomLocation(area: Area):
    x = random.uniform(area.xlowerlimit, area.xlimit)
    y = random.uniform(area.ylowerlimit, area.ylimit)
    return Location(x, y, area)


allowedareas = [Area(xlowerlimit=xlowerlim1, xlimit=xLim1, ylowerlimit=ylowerlim1, ylimit=yLim1),
                Area(xlowerlimit=xlowerlim2, xlimit=xLim2, ylowerlimit=ylowerlim2, ylimit=yLim2)]


def targetlocation(area: Area, lockdownFlag):
    chance = random.random()
    perc = 0 if lockdownFlag else .3
    if chance > perc:
        return randomLocation(area)
    else:
        return randomLocation(random.choice(allowedareas))
