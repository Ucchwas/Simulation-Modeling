import heapq
import matplotlib.pyplot as plt
import random
import math
from numpy.random import choice


def exponential(mean):
    return random.expovariate(1/mean)

def uni_random(lo,hi): 
    return random.uniform(lo, hi)

lazy = 0
busy = 1
simulation_duration = 5400

# mydict = dict()
# group_id = 0

Hot_Food = 0
Drinks = 2
Cashier = 3
Specialty_Sandwich = 1



# Parameters
class Params:
    def __init__(self, groups_of_size,groups_of_prob,arrival_time,runtime,routing, route_probability, employeesCount,ST_u,ACT_u):
        self.group_id = 0
        self.mydict = dict()
        self.lambd = arrival_time  # inter arrival rate
        self.group_size = groups_of_size  # service rate
        self.group_prob = groups_of_prob
        self.run_time = runtime
        self.routing = routing
        self.route_prob = route_probability
        self.st_u = ST_u
        self.act_u = ACT_u
        self.employee_count = employeesCount

        # Note lambd and mu are not mean value, they are rates i.e. (1/mean)


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.queue = []

        # Statistics
        self.util = 0.0
        self.avg_Q_delay = 0.0
        self.avg_Q_length = 0.0
        self.served = 0

        self.avg_cachier_q = 0
        self.avg_food_q = [0,0]
        self.max_food_q = [-math.inf, -math.inf]
        self.max_cachier_q = []
        self.server_status = []
        self.server_busy_count = []
        self.avg_cus_in_sys = 0
        self.max_cus = -math.inf

        # others
        self.total_delay = 0.0
        self.total_time_served = 0.0
        self.area_number_in_q = 0.0
        self.people_in_q = 0
        self.server_available = 0
        self.server_quantity = 0
        self.time_last_event = 0
        self.people_had_to_wait_in_q = 0
        self.total_customer_number = 0
        self.current_customer = 0

        self.customer_delay = [0,0,0]
        self.counter_delay = [0,0,0,0]
        self.server_counter = [0,0,0,0]
        self.cashier_busy_count = []

        self.total_arrival_customer_type = [0,0,0]
        self.avg_q_delay_counter = [0,0,0,0]
        self.avg_q_delay_customer = [0,0,0]
        self.total_customer_served = 0


    def update(self, sim, event):
        time_since_last_event = event.event_time - self.time_last_event
        self.time_last_event = event.event_time

        # self.area_number_in_q += (self.people_in_q * time_since_last_event)
        # self.total_time_served += time_since_last_event * ((sim.params.k - self.server_available) / sim.params.k)
        
        for i in range(sim.params.employee_count[3]) :
            self.avg_cachier_q += len(self.queue[3][i]) * time_since_last_event
        
        self.avg_cus_in_sys += self.current_customer * time_since_last_event
        self.avg_food_q[0] += len(self.queue[0]) * time_since_last_event
        self.avg_food_q[1] += len(self.queue[1]) * time_since_last_event

        for j in range(sim.params.employee_count[3]) :
            if len(self.queue[3][j]) > self.max_cachier_q[j] :
                self.max_cachier_q[j] = len(self.queue[3][j])

        if len(self.queue[0]) > self.max_food_q[0] :
            self.max_food_q[0] = len(self.queue[0])
        
        if len(self.queue[1]) > self.max_food_q[1] :
            self.max_food_q[1] = len(self.queue[1])

        if self.current_customer > self.max_cus :
            self.max_cus = self.current_customer

    # called when there's no event left
    # do the calculations here
    def finish(self, sim):
        try :
            for i in range(3) :
                self.avg_q_delay_customer[i] = self.customer_delay[i] / self.total_arrival_customer_type[i]
        except ZeroDivisionError :
            print('Zero Division Error')

        try :
            for i in range(4) :
                if i != 2 :
                    self.avg_q_delay_counter[i] = self.counter_delay[i] / self.server_counter[i]
        except ZeroDivisionError :
            print('Zero Division Error')
        # try:
        #     self.avg_Q_delay = self.total_delay / self.served
        # except ZeroDivisionError:
        #     print("error while determining avg q delay, served 0")

        # # sim.now() will have the EXIT time
        # self.util = self.total_time_served / sim.now()

        # # average q length
        # self.avg_Q_length = self.area_number_in_q / sim.now()
        self.avg_food_q[0] = self.avg_food_q[0] / sim.simulator_clock
        self.avg_food_q[1] = self.avg_food_q[1] / sim.simulator_clock
        self.avg_cus_in_sys = self.avg_cus_in_sys / sim.simulator_clock
        self.avg_cachier_q = self.avg_cachier_q / (sim.params.employee_count[3]*sim.simulator_clock)

        print('\nCachier Counter Queue No\tMaximum Queue Length')
        for i in range(sim.params.employee_count[3]):
            print(i,'\t\t\t\t',self.max_cachier_q[i])

        print('\nFood Counter No\t\tMaximum Queue Length')
        for i in range(2):
            print(i,'\t\t\t\t',self.max_food_q[i])
        #print(0,'\t\t\t\t',self.max_food_q[0],'\n',1,'\t\t\t\t',self.max_food_q[1])

        print('\nFood Counter No\t\tAverage Queue Length')
        for i in range(2):
            print(i,'\t\t\t',self.avg_food_q[i])
        #print(0,'\t\t\t\t',self.avg_food_q[0],'\n',1,'\t\t\t\t',self.avg_food_q[1])

        print('\n\nCashier counter average queue length\t:',self.avg_cachier_q)

        print('\nCustomer Type\t\tAverage queue delay')
        for i in range(3):
            print(i,'\t\t\t',self.avg_q_delay_customer[i])

        print('\nCounter No.\t\tAverage queue delay')
        for i in range(4):
            if i!=2:
                print(i,'\t\t\t',self.avg_q_delay_counter[i]) 
        

        print('\nMaximum customers in system', self.max_cus)
        print('Average number of customers', self.avg_cus_in_sys)
        print('Overall Delay',self.total_delay / 60)

        #print('\nFinal global group_id',sim.params.group_id)
        print('\nTotal customers arrived ',self.total_customer_number)
        print('Total customers served ',self.total_customer_served)



    #def print_results(self, sim):
        # DO NOT CHANGE THESE LINES
        # print('MMk Results: lambda = %lf, mu = %lf, k = %d' % (sim.params.lambd, sim.params.mu, sim.params.k))
        # print('MMk Total customer served: %d' % self.served)
        # print('MMk Average queue length: %lf' % self.avg_Q_length)
        # print('MMk Average customer delay in queue: %lf' % self.avg_Q_delay)
        # print('MMk Time-average server utility: %lf' % self.util)
        #pass

    #def get_results(self, sim):
        # return self.avg_Q_length, self.avg_Q_delay, self.util
        #pass


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.event_time = None
        self.queueNum = None 
        self.route = None
        self.gid = None
        self.groupNum = None
        self.customerType = None
        self.current_counter = None

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
        self.queueNum = None
        self.route = None
        self.gid = None
        self.groupNum = None
        self.type_of_customer = None
        self.current_counter = None


    def process(self, sim):
        # the server has started, next there will be an arrival, so we schedule the first arrival here
        # mydict[group_id] = 'no'
        grp = choice(sim.params.group_size, p = sim.params.group_prob)
        sim.params.mydict[sim.params.group_id] = 'UNUSED'

        for i in range(grp):
            q_num = 0
            current_counter = 0
            type_of_customer = choice([0,1,2], p = sim.params.route_prob)
            
            rt = sim.params.routing[type_of_customer]
            arrival_time = self.event_time + exponential(self.sim.params.lambd)
            self.sim.schedule_event(ArrivalEvent(arrival_time, sim, grp, current_counter, q_num, rt, type_of_customer, sim.params.group_id))

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
    def __init__(self, event_time, sim, grp, current_counter, q_num, rt, type_of_customer, group_id):
        super().__init__(sim)
        self.event_time = event_time
        self.eventType = 'ARRIVAL'
        self.sim = sim
        self.route = rt
        self.type_of_customer = type_of_customer
        self.gid = group_id
        self.groupNum = grp
        self.current_counter = current_counter
        self.queueNum = q_num
        

    def process(self, sim):
        sim.states.total_arrival_customer_type[self.type_of_customer] += 1 
        counter = self.route[self.current_counter]
        sim.states.total_customer_number += 1
        # schedule next arrival
        # next_arrival_time = sim.now() + exponential(sim.params.lambd)
        # sim.schedule_event(ArrivalEvent(next_arrival_time, sim))

        # # all the servers are busy, so the customer will have to wait in the queue
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
        if (sim.states.server_busy_count[3] == sim.params.employee_count[3] and counter == 3):
            #print('Cachier Queue')
            min_q = 0
            min_length = math.inf
            for i in range(sim.params.employee_count[3]):
                if len(sim.states.queue[3][i]) < min_length :
                    min_length = len(sim.states.queue[3][i])
                    min_q = i

            sim.states.queue[3][min_q].append(self)
            
            self.queueNum = min_q
        
        elif (sim.states.server_busy_count[counter] > 0 and (counter == 0 or counter == 1)):
            #print('Food Queue')
            sim.states.queue[counter].append(self)

                # sim.states.people_in_q += 1
                # sim.states.queue.append(self.event_time)
        else:
            d = 0.0
            #sim.states.total_delay += d
            sim.states.server_counter[counter] += 1
            sim.states.server_busy_count[counter] += 1
            # for i in range(sim.params.k):
            #     if sim.states.server_status[i] == lazy :
            #         sim.states.server_status[i] = busy
            #         break
            # sim.states.served += 1
            if counter == 3 :
                if self.type_of_customer != 2:
                    depart_time = uni_random(sim.params.act_u[2][0], sim.params.st_u[2][1]) + uni_random(sim.params.act_u[self.type_of_customer][0], sim.params.st_u[self.type_of_customer][1]) + self.event_time
                else :
                    depart_time = uni_random(sim.params.act_u[2][0], sim.params.st_u[2][1]) + self.event_time
            # depart_time = self.event_time + exponential(sim.params.mu)
            # sim.schedule_event(DepartureEvent(depart_time, sim))
                for i in range(sim.params.employee_count[3]) :
                    if sim.states.cashier_busy_count[i] == 0 :
                        self.queueNum = i
                        sim.states.cashier_busy_count[i] = 1
                        break
                sim.schedule_event(DepartureEvent(depart_time, sim, self.groupNum, self.type_of_customer,self.current_counter,self.queueNum,self.route,self.gid))    
            else :
                depart_time = uni_random(sim.params.st_u[counter][0], sim.params.st_u[counter][1]) + self.event_time
                sim.schedule_event(DepartureEvent(depart_time, sim, self.groupNum, self.type_of_customer,self.current_counter,self.groupNum,self.route,self.gid))

        if self.current_counter == 0 :
            sim.states.current_customer += 1
            sim.states.total_customer_number += 1
            
            if (self.gid in sim.params.mydict) and (sim.params.mydict[self.gid] == "UNUSED") :
                sim.params.mydict[self.gid] = "USED"
                grp = choice(sim.params.group_size, p = sim.params.group_prob)
                # global group_id
                # group_id += 1
                sim.params.group_id += 1
                sim.params.mydict[sim.params.group_id] = "UNUSED"
                # mydict[group_id] = 'no'
                # print('Ucc')
                for i in range(grp):
                    q_num = 0
                    current_counter = 0
                    type_of_customer = choice([0,1,2], p = sim.params.route_prob)
                    rt = sim.params.routing[type_of_customer]

                    arrival_time = self.event_time + exponential(self.sim.params.lambd)
                    sim.schedule_event(ArrivalEvent(arrival_time, sim, grp, current_counter, q_num, rt, type_of_customer, sim.params.group_id))    


class DepartureEvent(Event):
    def __init__(self, event_time, sim, groupNum, type_of_customer, current_counter, queueNum, route, gid):
        super().__init__(sim)
        self.event_time = event_time
        self.eventType = 'DEPARTURE'
        self.sim = sim
        self.queueNum = queueNum
        self.type_of_customer = type_of_customer
        self.groupNum = groupNum
        self.current_counter = current_counter
        self.gid = gid
        self.route = route

    def process(self, sim):
        counter = self.route[self.current_counter]
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
        if (counter == 3) and (len(sim.states.queue[3][self.queueNum]) == 0)  :
            sim.states.cashier_busy_count[self.queueNum] = 0
            sim.states.server_busy_count[counter] -= 1
        
        elif (len(sim.states.queue[counter]) == 0) and (counter == 1 or counter == 0) :
            sim.states.server_busy_count[counter] = 0
        
        else :
            # depart_time
            if counter != 2:
                #print("counter not 2")
                if counter == 3 :
                    if self.type_of_customer != 2 : 
                         depart_time = uni_random(sim.params.act_u[2][0], sim.params.st_u[2][1]) + uni_random(sim.params.act_u[self.type_of_customer][0], sim.params.st_u[self.type_of_customer][1]) + self.event_time
                    else :
                        depart_time = uni_random(sim.params.act_u[2][0], sim.params.st_u[2][1]) + self.event_time                    

                    p_ev = sim.states.queue[counter][self.queueNum].pop(0)
                
                elif counter == 1 or counter == 0 :
                    depart_time = uni_random(sim.params.st_u[counter][0], sim.params.st_u[counter][1]) + self.event_time
                    p_ev = sim.states.queue[counter].pop(0)
                
                sim.states.server_counter[counter] += 1
                d = self.event_time - p_ev.event_time
                sim.states.total_delay += d
                sim.states.customer_delay[p_ev.type_of_customer] += d
                # print("Ucc")
                sim.states.counter_delay[counter] += d
                sim.schedule_event(DepartureEvent(depart_time, sim, self.groupNum, self.type_of_customer, self.current_counter, self.queueNum, self.route, self.gid))

        if self.current_counter != len(self.route)-1 :
            # sim.states.people_in_q -= 1
            # delay = self.event_time - sim.states.queue.pop(0)
            # sim.states.total_delay += delay
            # sim.states.served += 1
            depart_time = self.event_time 
            current_counter = self.current_counter + 1
            sim.schedule_event(ArrivalEvent(depart_time, sim, self.groupNum, current_counter,self.queueNum, self.route, self.type_of_customer,self.gid))
        else :
            # for i in range(sim.params.k):
            #     if sim.states.server_status[i] == busy :
            #         sim.states.server_status[i] = lazy
            sim.states.total_customer_served += 1
            sim.states.current_customer -= 1



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

        for i in range(self.params.employee_count[3]):
            self.states.max_cachier_q.append(-math.inf)

        # self.states.server_available = self.params.k
        # self.states.server_quantity = self.params.k
        for i in range(4):
            self.states.queue.append([])
            if i == 0 or i ==1 :
                self.params.act_u[i][0] = self.params.act_u[i][0] / self.params.employee_count[i]
                self.params.act_u[i][1] = self.params.act_u[i][1] / self.params.employee_count[i]
                self.params.st_u[i][0] = self.params.st_u[i][0] / self.params.employee_count[i]
                self.params.st_u[i][1] = self.params.st_u[i][1] / self.params.employee_count[i]
            elif i == 3 :
                for j in range(self.params.employee_count[i]):
                    self.states.queue[i].append([])

        for i in range(4):
            self.states.server_busy_count.append(0)
            if i == 3 :
                for j in range(self.params.employee_count[3]):
                    self.states.cashier_busy_count.append(0)



    # returns the current time
    def now(self):
        return self.simulator_clock

    def schedule_event(self, event):
        heapq.heappush(self.eventQ, (event.event_time, event))

    def run(self):
        random.seed(self.seed)
        self.initialize()

        while len(self.eventQ) > 0:
            time, event = heapq.heappop(self.eventQ)

            if event.eventType == 'EXIT':
                break

            if self.states is not None:
                self.states.update(self, event)

            # print('Time:', round(event.event_time, 5), '| Event:', event)

            self.simulator_clock = event.event_time
            event.process(self)

        self.states.finish(self)
        print()

    # def isBusy(self):
    #     isbusy = True
    #     for i in range(self.params.k):
    #         if self.states.server_status[i] == lazy:
    #             isbusy = False
    #             break
    #     return isbusy

    # def busyCount(self):
    #     count = 0
    #     for i in range(self.params.k):
    #         if self.states.server_status[i] == busy:
    #             count += 1
    #     return count   

    # def print_results(self):
    #     self.states.print_results(self)

    # def get_results(self):
    #     return self.states.get_results(self)

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



def taskTwo():
    groups_of_size = [1,2,3,4]
    groups_of_prob = [0.5, 0.3, 0.1, 0.1]

    routing = [[0,2,3],[1,2,3],[2,3]]
    route_probability = [ 0.80, 0.15,  0.05]
    
    employeesCount = [1,2,0,2]
    
    ST_u = [[50,120],[60,180],[5,20]]
    ACT_u = [[20,40],[5,15],[5,10]]
    
    arrival_time = 30
    runtime = 90*60

    seed = 101
    sim = Simulator(seed)
    sim.configure(Params(groups_of_size,groups_of_prob,arrival_time,runtime,routing,route_probability,employeesCount,ST_u,ACT_u), States())
    sim.run()

def main():
    taskTwo()


if __name__ == "__main__":
    main()

