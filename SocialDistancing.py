# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:27:28 2020

@author: Suri
"""

import pygame

from Person import *
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation as anim
import pandas as pd
import time
from Pygamtesttarget import *

def initializeSD(popSize, infectedPercentage, sickPercentage, xlowerlimit, xLimit, ylowerlimit, yLimit, SDPercentage):
    population = initialize(popSize, infectedPercentage, sickPercentage, xlowerlimit, xLimit, ylowerlimit, yLimit)
    SDNum = int(np.floor(popSize * SDPercentage / 100))
    SDPeople = population.sample(n=SDNum).index.values.tolist()

    for index in SDPeople:
        population.at[index, 'Person'].doSocialDistancing()
    return population

