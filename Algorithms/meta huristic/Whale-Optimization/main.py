from objects import *
from optimizer import WhaleOptimizationScheduling
import numpy as np

def whale():
    tasks_np = np.load('./Comparesion/dataset/output/tasks.npy')
    resources_np = np.load('./Comparesion/dataset/output/resources.npy')

    tasks = []
    resources = []

    for i in range(tasks_np.shape[0]):
        temp_task = Task(id=int(tasks_np[i,0] - 1),computation_cost=tasks_np[i,1],deadline=tasks_np[i,3], input_size=tasks_np[i,5],output_size=tasks_np[i,6])
        tasks.append(temp_task)

    for i in range(resources_np.shape[0]):
        temp_resource = Resource(id=int(resources_np[i,0]),processing_speed=resources_np[i,2],energy_efficiency=resources_np[i,3],capacity=resources_np[i,1],type=resources_np[i,5])
        resources.append(temp_resource)

    lambda_penalty = 100

    woa_scheduler = WhaleOptimizationScheduling(tasks, resources, num_whales=30, max_iter=100)
    best_schedule, best_fitness = woa_scheduler.optimize()
    results = []

    print("Best task schedule (task -> resource):")
    for task_idx, resource_idx in enumerate(best_schedule):
        resource = resources[resource_idx]
        task = tasks[task_idx]
        t, e = calc_time_energy(task.computation_cost // resource.processing_speed + 1, (task.computation_cost // resource.processing_speed + 1) * resource.energy_efficiency,resource.type,
                                task.input_size,task.output_size)
        results.append((task.id, resource.id, t, e))
        # print(f"Task {task.id} -> Resource {resource.id} - Execution Time: {task.computation_cost / resource.processing_speed}, Energy:{task.computation_cost / resource.processing_speed * resource.energy_efficiency}")

    # print(f"Best fitness (total cost): {best_fitness}")

    results = np.array(results)
    np.save('./Comparesion/Algorithms/results/whale-results.npy',results)


whale()