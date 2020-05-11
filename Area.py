import numpy as np
import random


class Area:
    def __init__(self, xlimit, ylimit, name="Testarea"):
        self.xlimit = xlimit
        self.ylimit = ylimit
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
        return np.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def getDistanceLoc(self, other):
        return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

#    def getDistance(self, other):
 #       return np.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def getCopy(self):
        return Location(self.x, self.y, self.area)


# gives a random location inside a given area
def randomLocation(area: Area):
    x = random.uniform(0, area.xlimit)
    y = random.uniform(0, area.ylimit)
    return Location(x, y, area)
