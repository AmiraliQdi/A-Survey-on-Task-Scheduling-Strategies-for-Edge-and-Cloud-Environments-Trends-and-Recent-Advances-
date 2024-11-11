import numpy as np
from Agent import Agent
from objects import Task, Resource, calc_time_energy

tasks_np = np.load('./Comparesion/dataset/output/tasks.npy')
resources_np = np.load('./Comparesion/dataset/output/resources.npy')
cc_norm = 0.00000001
deadline_norm = 0.1

def reward_function(t, e):
    return 10 / (t + e)

def train():
    agent = Agent(input_size=4,output_size=resources_np.shape[0])

    avg_reward = []

    for task in tasks:
        if task.id % 500 == 0:
            print(f'task {task.id}, avg_reward:{np.mean(np.array(avg_reward))}')
            avg_reward = []
        task_tensor_data = task.to_tensor()
        action, pred = agent.act(task_tensor_data.unsqueeze(dim=1).view(1,-1))

        selected_device = resources[action]

        estimate_time = ( (task.computation_cost/cc_norm) // selected_device.proccesing_speed) + 1
        estimate_energy = estimate_time * selected_device.energy_efficiency
        t, e = calc_time_energy(estimate_time, estimate_energy, selected_device.type,task.input_size/cc_norm,task.output_size/cc_norm)
        if selected_device.can_execute(e):
            r = reward_function(t, e)
            avg_reward.append(r)
        else:
            r = -100
        agent.add_experience((task_tensor_data.unsqueeze(dim=1).view(1,-1),action,r))
        agent.experience_replay()
    
    agent.save('./Comparesion/Algorithms/Drl/agent.h5')

def test():
    agent = Agent(input_size=4,output_size=resources_np.shape[0])
    agent.load('./Comparesion/Algorithms/Drl/agent.h5')
    result = []

    for task in tasks:
        selected_device_id, _ = agent.act(task.to_tensor().unsqueeze(dim=1).view(1,-1))
        selected_device = resources[selected_device_id]
        estimate_time = ( (task.computation_cost / cc_norm) // selected_device.proccesing_speed) + 1
        estimate_energy = estimate_time * selected_device.energy_efficiency
        t, e = calc_time_energy(estimate_time, estimate_energy, selected_device.type,task.input_size/cc_norm,task.output_size/cc_norm)
        result.append((task.id, selected_device.id, t, e))

    np.save('./Comparesion/Algorithms/results/drl-results.npy',np.array(result))

tasks = []
resources = []

for i in range(tasks_np.shape[0]):
    temp_task = Task(id=int(tasks_np[i,0] - 1),computation_cost=tasks_np[i,1]*cc_norm,deadline=tasks_np[i,3] * deadline_norm,input_size=tasks_np[i,5]*cc_norm,output_size=tasks_np[i,6]*cc_norm, priority=tasks_np[i,4])
    tasks.append(temp_task)

for i in range(resources_np.shape[0]):
    temp_resource = Resource(id=int(resources_np[i,0]),processing_speed=resources_np[i,2]
                             ,energy_efficiency=resources_np[i,3],capacity=resources_np[i,1],type=resources_np[i,5])
    resources.append(temp_resource)

test()