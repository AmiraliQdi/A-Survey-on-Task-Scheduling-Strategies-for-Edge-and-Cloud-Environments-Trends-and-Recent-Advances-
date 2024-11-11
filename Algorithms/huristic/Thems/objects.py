

class Task_drl:
    def __init__(self, id, computation_cost, deadline, input_size, output_size, priority):
        self.id = id
        self.computation_cost = computation_cost
        self.deadline = deadline
        self.input_size = input_size
        self.output_size = output_size
        self.priority = priority


class Resource:
    def __init__(self, id, type,capacity, energy_efficiency, processing_speed):
        self.id = id
        self.type = type
        self.capacity = capacity
        self.energy_efficiency = energy_efficiency
        self.proccesing_speed = processing_speed

    def can_execute(self, energy):
        return self.capacity >= energy

    def execute(self, energy):
        self.capacity -= energy

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
