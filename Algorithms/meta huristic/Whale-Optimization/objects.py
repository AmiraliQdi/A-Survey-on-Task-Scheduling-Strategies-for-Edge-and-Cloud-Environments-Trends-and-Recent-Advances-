class Task:
    def __init__(self, id, computation_cost, deadline, input_size, output_size):
        self.id = id
        self.computation_cost = computation_cost
        self.deadline = deadline
        self.input_size = input_size
        self.output_size = output_size

class Resource:
    def __init__(self, id, capacity, energy_efficiency, processing_speed, type):
        self.id = id
        self.capacity = capacity
        self.energy_efficiency = energy_efficiency
        self.processing_speed = processing_speed
        self.max_capacity = capacity
        self.type = type

    def can_execute(self, energy, task):
        return self.capacity >= energy or task.deadline < task.computation_cost // self.processing_speed + 1

    def execution_time(self, task):
        return task.computation_cost // self.processing_speed + 1

    def execute(self, e):
        self.capacity -= e

    def reset(self):
        self.capacity = self.max_capacity


def calc_time_energy(proc_time, energy, device_type, task_input,task_output):
    timeTransMec = 0
    timeTransCC = 0
    baseTime = 0
    baseEnergy = 0
    totalEnergy = 0
    totalTime = 0

    transferRate5g =1e9
    latency5g=5e-3
    transferRateFiber =1e10
    latencyFiber=1e-3

    timeDownMec = task_input / transferRate5g
    timeDownMec += latency5g
    timeUpMec = task_output / transferRate5g
    timeUpMec += latency5g

    alpha = 52e-5
    beta = 3.86412
    powerMec = alpha * 1e9 / 1e6 + beta

    timeDownCC = task_output / transferRateFiber
    timeDownCC += latencyFiber
    timeUpCC = task_input / transferRateFiber
    timeUpCC += latencyFiber

    powerCC = 3.65 

    baseTime = proc_time
    baseEnergy = energy
    if device_type == 1:
        timeTransMec =  timeUpMec +  timeDownMec 
        energyTransMec = powerMec *  timeTransMec
        totalTime = baseTime + timeTransMec 
        totalEnergy =  baseEnergy + energyTransMec

    elif device_type == 2:
        timeTransMec =  timeUpMec +  timeDownMec 
        energyTransMec = powerMec * timeTransMec
        
        timeTransCC = timeUpCC+timeDownCC
        energyTransCC =  powerCC * timeTransCC
        
        totalTime =  baseTime + timeTransMec +timeTransCC

        totalEnergy = baseEnergy + energyTransMec + energyTransCC
    else:
        return baseTime, baseEnergy

    return totalTime , totalEnergy
