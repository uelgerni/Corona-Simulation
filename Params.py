# testing parameters for all sims
contagionDist = 5  # distance where spread is possible
contagionP = 100  # chance to spread when in reach
iPerc = 2  # percentage infected with no symptoms start
sPerc = 1  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
popsize1 = 75
popsize2 = 75

duration = 150 # duration of disease if normal course of disease (sick/infected, not critical)
testcap = 10  # capscity for coronatests
testper = 2  # how many iterations until there are new tests

xlowerlim, xLim, ylowerlim, yLim = 400, 800, 0, 600  # area size
