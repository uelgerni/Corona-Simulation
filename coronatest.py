from Person import Health
from enum import Enum


class Testresult(Enum):
    HEALTHY = 'healthy'  # snegative testresult
    INFECTED = 'infected'  # positive testresult
    NOTEST = 'notest'   # did not test

class Coronatest:



    def __init__(self, testcapacity = 0, testperiod = 2):
        self.capacity = testcapacity
        self.period = testperiod
        self.restcap = 0
        self.restperiod = self.period

    def update(self):
        self.restperiod = self.restperiod -1
        if self.restperiod == 0:
            self.restperiod = self.period
            self.restcap = self.capacity

    def persontest (self, health: Health ):
        # returns Testresult
        if self.restcap == 0:
            return Testresult.NOTEST
        if health == Health.HEALTHY:
            self.restcap = self.restcap-1
            return Testresult.HEALTHY
        elif health == Health.RECOVERED:
            self.restcap = self.restcap-1
            return Testresult.HEALTHY
        else:
            self.restcap = self.restcap-1
            return Testresult.INFECTED

#coronatest = Coronatest(3,2)
#coronatest.updatetest()
#x = coronatest.persontest(Health.HEALTHY)
#coronatest.updatetest()
#x = coronatest.persontest(Health.HEALTHY)
#x = coronatest.persontest(Health.RECOVERED)
#x = coronatest.persontest(Health.INFECTED)
#x = coronatest.persontest(Health.HEALTHY)
