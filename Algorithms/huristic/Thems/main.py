from objects import *
import numpy as np

def calculate_energy(task, resource):
    return (task.computation_cost // resource.proccesing_speed + 1),(task.computation_cost // resource.proccesing_speed + 1) * resource.energy_efficiency


def schedule_workflow_tasks(tasks, resources):
    tasks.sort(key=lambda t: t.deadline)

    schedule = []

    for task in tasks:
        suitable_resource = None
        min_value = float('inf')
        best_min_energy = 0
        best_min_time = 0
        for resource in resources:
            estimated_time, estimated_energy = calculate_energy(task, resource)
            time, energy = calc_time_energy(estimated_time,estimated_energy,resource.type,task.input_size,task.output_size)
            if resource.can_execute(energy):
                if energy + time > 1000:
                    print(resource.id, )
                if energy + time < min_value:
                    best_min_energy = energy
                    best_min_time = time
                    min_value = energy + time
                    suitable_resource = resource

        if suitable_resource:
            energy_used = best_min_energy
            execution_time = best_min_time
            suitable_resource.execute(energy_used)
            schedule.append((task.id, suitable_resource.id, execution_time, energy_used))
        else:
            print(f"Task {task.id} cannot be scheduled due to lack of resources.")

    return schedule

tasks_np = np.load('./Comparesion/dataset/output/tasks.npy')
resources_np = np.load('./Comparesion/dataset/output/resources.npy')

tasks = []
resources = []

for i in range(tasks_np.shape[0]):
    temp_task = Task(id=int(tasks_np[i,0] - 1),computation_cost=tasks_np[i,1],deadline=tasks_np[i,3],input_size=tasks_np[i,5],output_size=tasks_np[i,6], priority=tasks_np[i,4])
    tasks.append(temp_task)

for i in range(resources_np.shape[0]):
    temp_resource = Resource(id=int(resources_np[i,0]),processing_speed=resources_np[i,2]
                             ,energy_efficiency=resources_np[i,3],capacity=resources_np[i,1],type=resources_np[i,5])
    resources.append(temp_resource)

schedule = schedule_workflow_tasks(tasks, resources)
results = []

for entry in schedule:
    results.append((entry[0],entry[1],entry[2],entry[3]))
    # print(f"Task {entry[0]} is scheduled on Resource {entry[1]} with energy consumption of {entry[2]} units.")


results = np.array(results)
np.save('./Comparesion/Algorithms/results/thems-results.npy',results)