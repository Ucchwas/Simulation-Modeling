"""
The task is to simulate an M/M/k system with a single queue.
Complete the skeleton code and produce results for three experiments.
The study is mainly to show various results of a queue against its ro parameter.
ro is defined as the ratio of arrival rate vs service rate.
For the sake of comparison, while plotting results from simulation, also produce the analytical results.
"""

import heapq
import random
import numpy as np
import matplotlib.pyplot as plt


def isServerBusy(sim):
    res = True
    for i in range(sim.params.k):
        if sim.states.serverStatus[i] == 0:
            res = False
            break
    return res


# Parameters
class Params:
    def __init__(self, lambd, mu, k):
        self.lambd = lambd  # interarrival rate
        self.mu = mu  # service rate
        self.k = k
    # Note lambd and mu are not mean value, they are rates i.e. (1/mean)

# Write more functions if required


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.queue = []
        # Declare other states variables that might be needed

        # Statistics
        self.util = 0.0
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0
        self.prevArrivalTime = 0
        self.serverStatus = []
        self.qArea = 0
        self.lastEventTime = 0 
        self.totalDelay = 0
        self.totalCustomer = 0
        self.serverBusyTime = 0
        self.time_since_last_event = 0

    def update(self, sim, event):
        # Complete this function
        #print('len',len(self.queue))
        #if event.eventType == 'ARRIVAL':
         #   self.queue.append(event.eventTime)
        if event.eventType == 'DEPART':
            self.served += 1
        if isServerBusy(sim):
            self.serverBusyTime += self.time_since_last_event
        self.time_since_last_event = sim.simclock-self.lastEventTime
        self.lastEventTime = sim.simclock
        self.totalDelay += len(self.queue)*(self.time_since_last_event)
        if event.eventType == 'ARRIVAL':
            self.queue.append(event.eventTime)
            self.qArea += len(self.queue)*(self.time_since_last_event)
            #self.totalCustomer += 1
            if isServerBusy(sim) == False:
                for i in range(sim.params.k):
                    if sim.states.serverStatus[i] == 0:
                        sim.states.serverStatus[i] = 1
                        break
            self.totalCustomer += 1
        elif event.eventType == 'DEPART' and len(self.queue) == 0 :
            for i in range(sim.params.k):
                    if sim.states.serverStatus[i] > 0:
                        sim.states.serverStatus[i] = 0
                        break
        None

    def finish(self, sim):
        # Complete this function
        #print('total:',self.served)
        self.avgQdelay = self.totalDelay/self.totalCustomer
        #print('TotalDelay:',self.totalDelay)
        #print('TotalCustomer:',self.totalCustomer)
        #print('AVG:',self.avgQdelay)
        self.avgQlength = self.qArea/sim.simclock
        #print('AvgQlength:',self.avgQlength)
        self.util = self.serverBusyTime/sim.simclock
        None

    def printResults(self, sim):
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))

    def getResults(self, sim):
        return (self.avgQlength, self.avgQdelay, self.util)

# Write more functions if required


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None

    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def __repr__(self):
        return self.eventType


class StartEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim

    def process(self, sim):
        # Complete this function
        x = np.random.exponential(1/sim.params.lambd,1)
        t = sim.states.prevArrivalTime + x[0]
        sim.states.prevArrivalTime = t
        sim.scheduleEvent(ArrivalEvent(t,sim))
        sim.scheduleEvent(ExitEvent(100,sim))
        y = np.random.exponential(1/sim.params.mu,1)
        sim.scheduleEvent(DepartureEvent(t + y,sim))
        sim.states.totalCustomer += 1
        None


class ExitEvent(Event):
    def __init__(self, eventTime, sim):
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim

    def process(self, sim):
        # Complete this function
        None


class ArrivalEvent(Event):
    # Write __init__ function
    def __init__(self,eventTime,sim):
        self.eventTime = eventTime
        self.eventType = 'ARRIVAL'
        self.sim = sim
    def process(self, sim):
        # Complete this function
        x = np.random.exponential(1/sim.params.lambd,1)
        t = sim.states.prevArrivalTime + x[0]
        sim.states.prevArrivalTime = t
        sim.states.totalCustomer += 1
        #print('T----------',sim.states.prevArrivalTime)
        sim.scheduleEvent(ArrivalEvent(t,sim))
        None


class DepartureEvent(Event):
    # Write __init__ function
    def __init__(self,eventTime,sim):
        self.eventTime = eventTime
        self.eventType = 'DEPART'
        self.sim = sim
    def process(self, sim):
        # Complete this function
        if isServerBusy(sim):
            y = np.random.exponential(1/sim.params.mu,1)
            sim.scheduleEvent(DepartureEvent(sim.simclock + y,sim))
        None


class Simulator:
    def __init__(self, seed):
        self.eventQ = []
        self.simclock = 0
        self.seed = seed
        self.params = None
        self.states = None

    def initialize(self):
        self.simclock = 0
        self.scheduleEvent(StartEvent(0, self))

    def configure(self, params, states):
        self.params = params
        self.states = states
        for i in range(params.k):
            states.serverStatus.append(0)

    def now(self):
        return self.simclock

    def scheduleEvent(self, event):
        heapq.heappush(self.eventQ, (event.eventTime, event))

    def run(self):
        #print('Ucchwas')
        random.seed(self.seed)
        self.initialize()

        while len(self.eventQ) > 0:
            time, event = heapq.heappop(self.eventQ)

            if event.eventType == 'EXIT':
                #print('afshdaghdfjah')
                break

            if self.states != None:
                self.states.update(self, event)

            #print(event.eventTime, 'Event', event)
            self.simclock = event.eventTime
            event.process(self)
        #print('Ucchwas')
        self.states.finish(self)

    def printResults(self):
        self.states.printResults(self)

    def getResults(self):
        return self.states.getResults(self)


def experiment1():
    seed = 101
    sim = Simulator(seed)
    sim.configure(Params(5.0 / 60, 8.0 / 60, 1), States())
    #print('Ucchwas')
    sim.run()
    sim.printResults()


def experiment2():
    seed = 110
    mu = 1000.0 / 60
    ratios = [u / 10.0 for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []

    for ro in ratios:
        sim = Simulator(seed)
        sim.configure(Params(mu * ro, mu, 1), States())
        sim.run()

        length, delay, utl = sim.getResults()
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)

    plt.figure(1)
    plt.subplot(311)
    plt.plot(ratios, avglength)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q length')

    plt.subplot(312)
    plt.plot(ratios, avgdelay)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Avg Q delay (sec)')

    plt.subplot(313)
    plt.plot(ratios, util)
    plt.xlabel('Ratio (ro)')
    plt.ylabel('Util')

    plt.show()


def experiment3():
    seed = 110
    mu = 8.0 / 60
    lambd = 5.0 / 60
    k = [u for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []

    for ro in k:
        sim = Simulator(seed)
        sim.configure(Params(lambd, mu, ro), States())
        sim.run()

        length, delay, utl = sim.getResults()
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)

    plt.figure(1)
    plt.subplot(311)
    plt.plot(k, avglength)
    plt.xlabel('k (ro)')
    plt.ylabel('Avg Q length')

    plt.subplot(312)
    plt.plot(k, avgdelay)
    plt.xlabel('k (ro)')
    plt.ylabel('Avg Q delay (sec)')

    plt.subplot(313)
    plt.plot(k, util)
    plt.xlabel('k (ro)')
    plt.ylabel('Util')

    plt.show()
    # Similar to experiment2 but for different values of k; 1, 2, 3, 4
    # Generate the same plots
    # Fix lambd = (5.0/60), mu = (8.0/60) and change value of k
    None


def main():
    experiment1()
    experiment2()
    experiment3()


if __name__ == "__main__":
    main()