import random

# Task object class
class Task:
    def __init__(self, id, processing_time, base_energy, deadline, priority):
        self.id = id
        self.processing_time = processing_time
        self.base_energy = base_energy
        self.deadline = deadline
        self.priority = priority

    def to_dict(self):
        return {
        "task_id": self.i,
        "processing_time": self.processing_time,
        "base_energy": self.base_energy,
        "deadline": self.deadline,
        "priority": self.priority
        }

# Resource object class
class Resource:
    def __init__(self, id, capacity, efficiency_factor, execution_speed, idle_power):
        self.id = id
        self.max_cap = capacity
        self.capacity = capacity
        self.efficiency_factor = efficiency_factor
        self.execution_speed = execution_speed
        self.idle_power = idle_power
    
    def calculate_energy_consumption(self, task):
        return ( task.processing_time / self.execution_speed ) * self.efficiency_factors
    
    def calculate_execution_time(self, task):
        return task.processing_time / self.execution_speed
    
    def to_dict(self):
        return {
        "resource_id": self.id,
        "capacity": self.capacity,
        "efficiency_factor": self.efficiency_factor,
        "execution_speed": self.execution_speed,
        "idle_power": self.idle_power,
    }
