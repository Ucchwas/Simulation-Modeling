import heapq
import random
import math
#from lcgrand import *
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import choice


file = open("input.txt")

lines = file.readlines()

num_of_stations,k = 0 , 0
inter_arrival = 0.0
num_of_machines = []
job_pro = []
si = []
station_routing = []
mean_service_time = []
choice_arr = []

count,p = 0, 0
j = 0
for line in lines:
    if count == 0:
        var = line.split()
        num_of_stations = int(var[0])
    if count == 1:
        var = line.split()
        for i in range(num_of_stations):
            num_of_machines.append(int(var[i]))
    if count == 2:
        var = line.split()
        inter_arrival = float(var[0])
    if count == 3:
        var = line.split()
        k = int(var[0])
        for i in range(k):
            choice_arr.append(i)
    if count == 4:
        var = line.split()
        for i in range(k):
            job_pro.append(float(var[i]))
    if count == 5:
        var = line.split()
        for i in range(k):
            si.append(int(var[i]))
    if count > 5:
        data = []
        var = line.split()
        #print(line)
        if p == 0:
            for i in range(si[j]):
                data.append(int(var[i]))
            p = 1
            station_routing.append(data)
        else:
            for i in range(si[j]):
                data.append(float(var[i]))
            p = 0
            mean_service_time.append(data)
            j += 1
    count += 1


#print(num_of_stations)
#print(num_of_machines)
#print(inter_arrival)
#print(k)
#print(job_pro)
#print(si)
#print(station_routing)
#print(mean_service_time)


def exponential(rate):
    return random.expovariate(1/rate)
    #return -(1 / mean) * math.log(lcgrand(1))
def erlang(mean):
    return exponential(mean/2)+exponential(mean/2)


lazy = 0
busy = 1
simulation_duration = 8


# Parameters
class Params:
    def __init__(self,num_of_stations, num_of_machines, inter_arrival, k, job_pro, si, station_routing, mean_service_time):
        self.lambd = inter_arrival  # inter arrival rate
        self.mu = mean_service_time  # service rate
        self.num_station = num_of_stations
        self.num_machine = num_of_machines
        self.job_prob = job_pro
        self.num_si = si
        self.jobs = k
        self.routing = station_routing
        # Note lambd and mu are not mean value, they are rates i.e. (1/mean)


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.queue = []
        self.server_busy_count = []

        # Statistics
        self.util = 0.0
        self.avg_Q_delay = 0.0
        self.avg_Q_length = 0.0
        self.served = 0

        self.job_occurance = []
        self.station_delay = []
        self.job_delay = []
        self.station_served = []

        # others
        self.total_delay = 0.0
        self.total_time_served = 0.0
        #self.area_number_in_q = 0.0
        self.people_in_q = 0
        self.server_available = 0
        self.server_quantity = 0
        self.time_last_event = 0
        self.people_had_to_wait_in_q = 0
        self.server_status = []

        self.avgQLength = []
        self.avgQDelay = []

        self.current_jobs = 0
        self.area_number_jobs = 0
        self.avg_number_jobs = 0
        self.avg_job_delay = []
        self.overall_avg_delay = 0
        self.area_number_in_q = []


    def update(self, sim, event):
        time_since_last_event = event.event_time - self.time_last_event
        # self.time_last_event = event.event_time

        # self.area_number_in_q += (self.people_in_q * time_since_last_event)
        # self.total_time_served += time_since_last_event * ((sim.params.k - self.server_available) / sim.params.k)
        if event.eventType != 'START' :
            self.area_number_in_q[event.currentStation-1] += len(sim.states.queue[event.currentStation-1]) * time_since_last_event
            self.area_number_jobs += self.current_jobs * time_since_last_event
        self.time_last_event = event.event_time

    # called when there's no event left
    # do the calculations here
    def finish(self, sim):
        # try:
        #     self.avg_Q_delay = self.total_delay / self.served
        # except ZeroDivisionError:
        #     print("error while determining avg q delay, served 0")

        # # sim.now() will have the EXIT time
        # self.util = self.total_time_served / sim.now()

        # # average q length
        # self.avg_Q_length = self.area_number_in_q / sim.now()

        for i in range(sim.params.num_station):
            self.avgQLength[i] = self.area_number_in_q[i] / (sim.simulator_clock)
            try:
                self.avgQDelay[i] = self.station_delay[i] / self.station_served[i]
            except ZeroDivisionError:
                print("Zero Division Error")
        self.avg_number_jobs = self.area_number_jobs / (sim.simulator_clock)

        for i in range(sim.params.jobs):
            try:
                self.avg_job_delay[i] = self.job_delay[i] / self.job_occurance[i]
            except ZeroDivisionError:
                print("Zero Division Error")
            self.overall_avg_delay += sim.params.job_prob[i] * self.avg_job_delay[i]    
            
        

    def print_results(self, sim):
        # DO NOT CHANGE THESE LINES
        # print('MMk Results: lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        # print('MMk Total customer served: %d' % self.served)
        # print('MMk Average queue length: %lf' % self.avg_Q_length)
        # print('MMk Average customer delay in queue: %lf' % self.avg_Q_delay)
        # print('MMk Time-average server utility: %lf' % self.util)
        print('\nAverage Delay in queue')
        for i in range(sim.params.num_station):
            print(self.avgQDelay[i])
        
        print('\nAverage Length in queue')
        for i in range(sim.params.num_station):
            print(self.avgQLength[i])
        
        print('\nAverage Job Delay')
        for i in range(sim.params.jobs):
            print(self.avg_job_delay[i])
        
        print('\nAverage Number Jobs', self.avg_number_jobs)

        print('\nOverall Average Delay',self.overall_avg_delay)



    def get_results(self, sim):
        #print(self.avgQLength, self.avgQDelay, self.avg_job_delay, self.avg_number_jobs, self.overall_avg_delay)
        return (self.avgQLength, self.avgQDelay, self.avg_job_delay, self.avg_number_jobs, self.overall_avg_delay)


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.event_time = None
        self.currentStation = None
        self.jobType = None
        self.station_index = None

    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def __repr__(self):
        return self.eventType


class StartEvent(Event):
    def __init__(self, event_time, sim):
        super().__init__(sim)
        self.event_time = event_time
        self.eventType = 'START'
        self.sim = sim

    def process(self, sim):
        # the server has started, next there will be an arrival, so we schedule the first arrival here
        jType = choice(choice_arr,p = job_pro)
        current_station = sim.params.routing[jType][0]

        station_index = 0
        arrival_time = self.event_time + exponential(sim.params.lambd)

        self.sim.schedule_event(ArrivalEvent(arrival_time, self.sim, jType, current_station, station_index))

        # set the exit event here
        self.sim.schedule_event(ExitEvent(simulation_duration, self.sim))


class ExitEvent(Event):
    def __init__(self, event_time, sim):
        super().__init__(sim)
        self.event_time = event_time
        self.eventType = 'EXIT'
        self.sim = sim

    def process(self, sim):
        print("simulation is going to end now. current time:", self.event_time)


class ArrivalEvent(Event):
    def __init__(self, event_time, sim, jType, current_station, station_index):
        super().__init__(sim)
        self.event_time = event_time
        self.eventType = 'ARRIVAL'
        self.sim = sim
        self.currentStation = current_station
        self.jobType = jType
        self.station_index = station_index

    def process(self, sim):
        # schedule next arrival
        # next_arrival_time = sim.now() + exponential(sim.params.lambd)
        # sim.schedule_event(ArrivalEvent(next_arrival_time, sim))
        if self.station_index == 0:
            sim.states.job_occurance[self.jobType] += 1
            sim.states.current_jobs += 1

            jType = choice(choice_arr, p = job_pro)
            current_station = sim.params.routing[jType][0]
            station_index = 0

            arrival_time = self.event_time + exponential(self.sim.params.lambd)
            sim.schedule_event(ArrivalEvent(arrival_time, sim, jType, current_station, station_index))

        # all the servers are busy, so the customer will have to wait in the queue
        # if sim.states.server_available <= 0:
        #     sim.states.people_in_q += 1
        #     sim.states.people_had_to_wait_in_q += 1
        #     sim.states.queue.append(sim.now())
        # else:
        #     delay = 0
        #     sim.states.total_delay += delay

        #     # use a free server
        #     sim.states.server_available -= 1
        #     sim.states.served += 1

        #     # schedule a departure
        #     depart_time = sim.now() + exponential(sim.params.mu)
        #     sim.schedule_event(DepartureEvent(depart_time, sim))
        if sim.isBusy(self.currentStation) == busy :
            sim.states.queue[self.currentStation-1].append(self)
            # sim.states.people_in_q += 1
            # sim.states.people_had_to_wait_in_q += 1
        else:
            # delay = 0
            # sim.states.total_delay += delay
            sim.states.server_busy_count[self.currentStation-1] += 1
            
            # sim.states.served += 1
            sim.states.station_served[self.currentStation-1] += 1

            depart_time = self.event_time + erlang(sim.params.mu[self.jobType][self.station_index])
            sim.schedule_event(DepartureEvent(depart_time, sim, self.jobType, self.currentStation, self.station_index)) 


class DepartureEvent(Event):
    def __init__(self, event_time, sim, jType, current_station, station_index):
        super().__init__(sim)
        self.event_time = event_time
        self.eventType = 'DEPARTURE'
        self.sim = sim
        self.jobType = jType
        self.currentStation = current_station
        self.station_index = station_index

    def process(self, sim):
        # if len(sim.states.queue) == 0:
        #     sim.states.server_available += 1

        #     if sim.states.server_available > sim.params.k:
        #         print("error !! server number exceeded total server number")

        # else:
        #     sim.states.people_in_q -= 1

        #     delay = sim.now() - sim.states.queue[0]
        #     sim.states.total_delay += delay

        #     sim.states.served += 1
        #     depart_time = sim.now() + exponential(sim.params.mu)
        #     sim.schedule_event(DepartureEvent(depart_time, sim))

        #     sim.states.queue.pop(0)
        if self.station_index == (sim.params.num_si[self.jobType]-1):
            sim.states.current_jobs -= 1
        else:
            jType = self.jobType
            station_index = self.station_index+1
            current_station = sim.params.routing[jType][station_index]
            arrival_time = self.event_time
            sim.schedule_event(ArrivalEvent(arrival_time, sim, jType, current_station, station_index))
        
        if len(sim.states.queue[self.currentStation-1]) == 0:
            sim.states.server_busy_count[self.currentStation-1] -= 1
        else:
            # sim.states.people_in_q -= 1
            pop_event = sim.states.queue[self.currentStation-1].pop(0)
            delay = self.event_time - pop_event.event_time
            sim.states.station_delay[self.currentStation-1] += 1
            sim.states.job_delay[self.jobType] += delay

            sim.states.total_delay += delay

            depart_time = self.event_time + erlang(sim.params.mu[self.jobType][self.station_index])
            sim.schedule_event(DepartureEvent(depart_time, sim, self.jobType, self.currentStation, self.station_index))

            sim.states.station_served[self.currentStation-1] += 1
            # sim.states.served += 1


class Simulator:
    def __init__(self, seed):
        # eventQ is a min heap, we are pushing events in it, when retrieved, it will give the next earliest event
        self.eventQ = []
        self.simulator_clock = 0
        self.seed = seed
        self.params = None
        self.states = None

    def initialize(self):
        self.simulator_clock = 0
        self.schedule_event(StartEvent(0, self))

    # adds the parameters like mu and lambda, a states object is initiated
    def configure(self, params, states):
        self.params = params
        self.states = states

        # self.states.server_available = self.params.k
        # self.states.server_quantity = self.params.k

        for i in range(self.params.num_station):
            self.states.station_served.append(0)
            self.states.station_delay.append(0)
            self.states.queue.append([])
            self.states.server_busy_count.append(0)
            self.states.area_number_in_q.append(0)
            self.states.avgQLength.append(0)
            self.states.avgQDelay.append(0)
        #print('Server busy count', self.states.server_busy_count)

        for i in range(self.params.jobs):
            self.states.job_occurance.append(0)
            self.states.job_delay.append(0)
            self.states.avg_job_delay.append(0)
        #print('Job occurance', self.states.job_occurance)

    # returns the current time
    def now(self):
        return self.simulator_clock

    def schedule_event(self, event):
        heapq.heappush(self.eventQ, (event.event_time, event))

    def run(self):
        #print('Ucchwas')
        random.seed(self.seed)
        self.initialize()

        while len(self.eventQ) > 0:
            time, event = heapq.heappop(self.eventQ)

            if event.eventType == 'EXIT':
                break

            if self.states is not None:
                self.states.update(self, event)

            # print('Time:', round(event.event_time, 5), '| Event:', event)
            # print(event.event_time, 'Event' , event)

            self.simulator_clock = event.event_time
            event.process(self)

        self.states.finish(self)
        #print()

    def print_results(self):
        self.states.print_results(self)

    def get_results(self):
        return self.states.get_results(self)

    def isBusy(self, current_station):
        isbusy = False
        if self.states.server_busy_count[current_station-1] >= self.params.num_machine[current_station-1]:
            isbusy =True
        return isbusy

    
    def print_analytical_results(self):
        # avg queue len = (lambda * lambda) / (mu * (mu - lambda))
        avg_q_len = (self.params.lambd * self.params.lambd) / (self.params.mu * (self.params.mu - self.params.lambd))

        # avg delay in queue = lambda / (mu * (mu - lambda))
        avg_delay_in_q = self.params.lambd / (self.params.mu * (self.params.mu - self.params.lambd))

        # server utilization factor = lambda / mu
        server_util_factor = self.params.lambd / self.params.mu

        print("\nAnalytical Results :")
        print("lambda = %lf, mu = %lf" % (self.params.lambd, self.params.mu))
        print("Average queue length", round(avg_q_len, 3))
        print("Average delay in queue", round(avg_delay_in_q, 3))
        print("Server utilization factor", round(server_util_factor, 3))

simulation_iterator = 30

def taskOne():
    final_avgQLength = [0] * (num_of_stations+1)
    final_avgQDelay = [0]*(num_of_stations+1)
    final_avg_job_delay = [0]*(k+1)
    final_avg_number_jobs = 0
    final_overall_avg_delay = 0.0
    for i in range(simulation_iterator):
        seed = 101
        sim = Simulator(seed)
        sim.configure(Params(num_of_stations, num_of_machines, inter_arrival, k, job_pro, si, station_routing, mean_service_time),States())
        sim.run()
        #sim.print_analytical_results()
        #sim.print_results()
        avgQLegth, avgQDelay, avg_job_delay, avg_number_jobs, overall_avg_delay = sim.get_results()

        for j in range(0,num_of_stations,1):
            final_avgQLength[j] += avgQLegth[j]
            final_avgQDelay[j] += avgQDelay[j]

        for j in range(0,k,1):
            final_avg_job_delay[j] += avg_job_delay[j]

        final_avg_number_jobs += avg_number_jobs
        final_overall_avg_delay += overall_avg_delay
    
    for j in range(0,k,1):
        final_avg_job_delay[j] /= simulation_iterator
    
    final_avg_number_jobs /= simulation_iterator
    final_overall_avg_delay /= simulation_iterator

    for j in range(0,num_of_stations,1):
        final_avgQLength[j] /= simulation_iterator
        final_avgQDelay[j] /= simulation_iterator


    print('\nAverage Delay in queue')
    for i in range(sim.params.num_station):
        print(final_avgQDelay[i])
        
    print('\nAverage Length in queue')
    for i in range(sim.params.num_station):
        print(final_avgQLength[i])
        
    print('\nAverage Job Delay')
    for i in range(sim.params.jobs):
        print(final_avg_job_delay[i])
        
    print('\nAverage Number Jobs', final_avg_number_jobs)

    print('\nOverall Average Delay',final_overall_avg_delay)


def main():
    taskOne()


if __name__ == "__main__":
    main()
