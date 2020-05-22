# testing parameters for all sims
contagionDist = 4  # distance where spread is possible
contagionP = 100  # chance to spread when in reach
iPerc = 2  # percentage infected with no symptoms start
sPerc = 1  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
popsize1 = 100
popsize2 = 100

duration = 100
testcap = 30  # capscity for coronatests
testper = 2  # how many iterations until there are new tests

xlowerlim, xLim, ylowerlim, yLim = 400, 800, 0, 600  # area size
