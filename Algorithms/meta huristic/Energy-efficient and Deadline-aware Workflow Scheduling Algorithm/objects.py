import random

# Task object class
class Task:
    def __init__(self, id, computation_cost, deadline, input_size, output_size):
        self.id = id
        self.computation_cost = computation_cost
        self.deadline = deadline
        self.input_size = input_size
        self.output_size = output_size

# Resource object class
class Resource:
    def __init__(self, id, processing_speed, energy_efficiency, type):
        self.id = id
        self.processing_speed = processing_speed
        self.energy_efficiency = energy_efficiency
        self.type = type
    
    def calculate_execution_time(self, task):
        return task.computation_cost // self.processing_speed + 1


    def calculate_energy_consumption(self, task):
        return ( task.computation_cost // self.processing_speed + 1) * self.energy_efficiency
    
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

