from gen import Generator
import numpy as np

tasks = Generator.get_tasks()
resources = Generator.get_devices()
jobs = Generator.get_jobs()

task_dataset = np.zeros((len(tasks),7))
resources_dataset = np.zeros((len(resources),6))

for i, task in enumerate(tasks):
    temp_task = []
    temp_task.append(task['id']) # 0
    temp_task.append(task['computational_load']) # 1
    temp_task.append(0) # 2
    temp_task.append(jobs[task['job_id']]['deadline'] // jobs[task['job_id']]['task_count']) # Deadline # 3
    temp_task.append(len(task['successors'])) # Priority # 4
    temp_task.append(task['input_size']) # input 5
    temp_task.append(task['output_size']) # output 6
    task_dataset[i,:] = np.array(temp_task)

for i, resource in enumerate(resources):
    temp_resource = []
    temp_resource.append(i) # 0
    temp_resource.append(resource['battery_capacity']) # 1 cap
    voltages_frequencies = np.array(resource['voltages_frequencies'])
    avg_vf = np.mean(voltages_frequencies[:,0],axis=0)
    temp_resource.append(avg_vf[0]) # 2 freq
    energy_cons = resource['capacitance'] * avg_vf[0] * avg_vf[1] * avg_vf[1]
    if resource['type'] == 'cloud':
        energy_cons = avg_vf[1]
    temp_resource.append(energy_cons) # 3 energy_cons
    temp_resource.append(0) # 4 idle
    if resource['type'] == 'iot': # type 5
        temp_resource.append(0)
    elif resource['type'] == 'mec':
        temp_resource.append(1)
    else:
        temp_resource.append(2)   
    resources_dataset[i,:] = np.array(temp_resource)
    

np.save('./Comparesion/dataset/output/tasks.npy',task_dataset)
np.save('./Comparesion/dataset/output/resources.npy',resources_dataset)
