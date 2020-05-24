from Person import Health
from enum import Enum


class Testresult(Enum):
    HEALTHY = 'healthy'  # negative testresult
    INFECTED = 'infected'  # positive testresult
    NOTEST = 'notest'  # did not test


class Coronatest:

    def __init__(self, testcapacity=0, testperiod=2):
        self.capacity = testcapacity
        self.period = testperiod
        self.restcap = 0
        self.restperiod = self.period

    def update(self):  #countdown untill testcapacity is recharged
        self.restperiod = self.restperiod - 1
        if self.restperiod == 0:
            self.restperiod = self.period
            self.restcap = self.capacity

    def persontest(self, health: Health):  # returns testresult, negative if person is healthy or recovered, positive if neither, no result if the testcapacity is empty
        if self.restcap == 0:
            return Testresult.NOTEST
        if health == Health.HEALTHY:
            self.restcap = self.restcap - 1
            return Testresult.HEALTHY
        elif health == Health.RECOVERED:
            self.restcap = self.restcap - 1
            return Testresult.HEALTHY
        else:
            self.restcap = self.restcap - 1
            return Testresult.INFECTED


