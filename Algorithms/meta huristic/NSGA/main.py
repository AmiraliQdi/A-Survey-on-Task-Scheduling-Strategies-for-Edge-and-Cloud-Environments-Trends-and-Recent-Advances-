import random
import numpy as np

npy_tasks = np.load('./Comparesion/dataset/output/tasks.npy')
npy_resources = np.load('./Comparesion/dataset/output/resources.npy')

NUM_TASKS = npy_tasks.shape[0]
NUM_RESOURCES = npy_resources.shape[0]
POPULATION_SIZE = 30
GENERATIONS = 100
MUTATION_RATE = 0.6

# Task and resource attributes setup
tasks = [
    {
        "task_id": int(npy_tasks[i,0])-1,
        "processing_time": npy_tasks[i,1],
        "base_energy": npy_tasks[i,2],
        "deadline": npy_tasks[i,3],
        "priority": npy_tasks[i,4],
        "input_size" : npy_tasks[i,5],
        "output_size" : npy_tasks[i,6]
    }
    for i in range(NUM_TASKS)
]

resources = [
    {
        "resource_id": int(npy_resources[i,0]),
        "capacity": npy_resources[i,1],
        'max_cap' : npy_resources[i,1],
        "efficiency_factor": npy_resources[i,3],
        "execution_speed": npy_resources[i,2],
        "idle_power": npy_resources[i,4],
        "type": npy_resources[i,5]
    }
    for i in range(NUM_RESOURCES)
]

print('Read resources and task sucessfuly')

# Semi-greedy initialization
def semi_greedy_initialization():
    population = []
    for _ in range(POPULATION_SIZE):
        schedule = []
        for task in tasks:
            available_resources = [r for r in resources if r["capacity"] >= (task["processing_time"] // r['execution_speed'] + 1) * r['efficiency_factor']]
            selected_resource = random.choice(available_resources) if available_resources else random.choice(resources)
            schedule.append((task["task_id"], selected_resource["resource_id"]))
        population.append(schedule)
    return population


# Enhanced fitness evaluation function
def evaluate_fitness(schedule):
    makespan = 0
    total_energy = 0
    total_time = 0
    missed_deadlines = 0
    resource_time = [0] * NUM_RESOURCES
    
    for task_id, resource_id in schedule:
        task = tasks[task_id]
        resource = resources[resource_id]
        
        # Calculate dynamic energy consumption based on resource efficiency
        execution_time = task["processing_time"] // resource["execution_speed"] + 1
        energy_consumption = execution_time * resource["efficiency_factor"]
        t, e = calc_time_energy(execution_time,energy_consumption,resource['type'],task['input_size'],task['output_size'])
        total_time += t
        
        # Check if task meets its deadline
        
        task_end_time = t
        if task_end_time > task["deadline"]:
            missed_deadlines += 1  # Track missed deadlines

        if e > resource['capacity']:
            missed_deadlines += 1

        resource['capacity'] -= e
        
        # Update resource time and total energy consumption
        ### TODO if want to add resource time , add execution_time instead of 0
        resource_time[resource_id] += t
        # If want the idle power too, add resource["idle_power"] here instead of 0
        total_energy += e + 0
        
    for _, resource_id in schedule:
        resource = resources[resource_id]
        resource['capacity'] = resource['max_cap']

    makespan = max(resource_time)  # Maximum time any resource takes
    return total_time, total_energy, missed_deadlines

# Non-dominated sorting for NSGA-II
def non_dominated_sorting(population):
    fronts = [[]]
    for i, p1 in enumerate(population):
        dominated = []
        dominates = 0
        for j, p2 in enumerate(population):
            f1 = evaluate_fitness(p1)
            f2 = evaluate_fitness(p2)
            if dominates_solution(f1, f2):
                dominated.append(j)
            elif dominates_solution(f2, f1):
                dominates += 1
        if dominates == 0:
            fronts[0].append(i)
    return fronts

# Check Pareto dominance
def dominates_solution(f1, f2):
    # Return True if f1 dominates f2 based on makespan, energy, and missed deadlines
    return (f1[0] <= f2[0] and f1[1] <= f2[1] and f1[2] < f2[2]) or (f1[0] < f2[0] and f1[1] < f2[1])

# Crossover function
def crossover(parent1, parent2):
    point = random.randint(0, NUM_TASKS - 1)
    child = parent1[:point] + parent2[point:]
    return child

# Mutation function
def mutate(schedule):
    if random.random() < MUTATION_RATE:
        task_idx = random.randint(0, NUM_TASKS - 1)
        new_resource = random.randint(0, NUM_RESOURCES - 1)
        schedule[task_idx] = (schedule[task_idx][0], new_resource)

# Main NSGA-II loop
def nsga_ii():
    population = semi_greedy_initialization()
    for generation in range(GENERATIONS):
        new_population = []
        ranks = non_dominated_sorting(population)
        
        # Add solutions from best fronts
        for front in ranks:
            if len(new_population) + len(front) <= POPULATION_SIZE:
                new_population.extend([population[i] for i in front])
            else:
                new_population.extend([population[i] for i in front[:POPULATION_SIZE - len(new_population)]])
                break

        # Generate offspring through crossover and mutation
        best_solution = None
        counter = 10
        while len(new_population) < POPULATION_SIZE:
            parent1 = random.choice(new_population)
            parent2 = random.choice(new_population)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            mutate(child1)
            mutate(child2)
            new_population.append(child1)
            new_population.append(child2)
            population = new_population[:POPULATION_SIZE]

        best_solution = min(population, key=evaluate_fitness)
        print(f"Generation {generation}: Best solution fitness: {evaluate_fitness(best_solution)}")

    make_output(best_solution)


def make_output(solution):
    results = []
# Display the best schedule
    for task_id, resource_id in solution:
        task = tasks[task_id]
        resource = resources[resource_id] 
        exec_time = task['processing_time'] // resource['execution_speed'] + 1
        energy = exec_time * resource['efficiency_factor']
        results.append((task['task_id'],resource['resource_id'],exec_time,energy))
        #print(f"Task {task.id} -> Resource {resource.id} - Execution Time: {exec_time:.2f}, Energy: {energy:.2f}")

    results = np.array(results)
    np.save('./Comparesion/Algorithms/results/NSGAII-results.npy',results)

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

        

# Run the enhanced NSGA-II algorithm
nsga_ii()
