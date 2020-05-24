# testing parameters for all sims
contagionDist = 5  # distance where spread is possible
contagionP = 100  # chance to spread when in reach
iPerc = 2  # percentage infected with no symptoms start
sPerc = 5  # percentage sick at start, those two groups will sometimes have an overlap, ergo fewer infected than infectedPercentage*n/100
popsize1 = 75
popsize2 = 75

duration = 150 # duration of disease if normal course of disease (sick/infected, not critical)
testcap = 0  # capacity for coronatests, set to zero if you dont want testing
testper = 2  # how many ticks until there are new tests

xmiddle, xLim, ylowerlim, yLim = 400, 800, 0, 600  # borders and middle of whole window
xlowerlim1, xLim1, ylowerlim1, yLim1 = 400, 800, 0, 600  # area1 borders
#xlowerlim2, xLim2, ylowerlim2, yLim2 = 300, 500, 200, 400  # area2 borders
xlowerlim2, xLim2, ylowerlim2, yLim2 = 0, 400, 0, 600  # area2 borders