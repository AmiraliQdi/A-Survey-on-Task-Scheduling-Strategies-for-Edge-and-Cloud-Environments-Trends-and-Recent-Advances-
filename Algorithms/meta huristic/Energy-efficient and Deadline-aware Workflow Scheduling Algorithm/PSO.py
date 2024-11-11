from objects import *
import numpy as np
# Initialize particles (schedules) - each particle is a potential solution
def initialize_particles(tasks, resources, num_particles):
    particles = []
    for _ in range(num_particles):
        particle = []  # Each particle represents a schedule (list of task-resource pairs)
        for task in tasks:
            assigned_resource = random.choice(resources)  # Randomly assign a resource
            particle.append((task, assigned_resource))
        particles.append(particle)
    return particles

# Calculate fitness function (total energy and penalty for missing deadlines)
def calculate_fitness(particle):
    total_energy = 0
    deadline_penalty = 0
    penalty_factor = 1000  # High penalty for deadline violations
    
    for task, resource in particle:
        execution_time = resource.calculate_execution_time(task)
        e = resource.calculate_energy_consumption(task)
        total_energy += e
        time, energy = calc_time_energy(execution_time,e,resource.type,task.input_size,task.output_size)
        if time > task.deadline:
            deadline_penalty += 1  # Penalty if deadline exceeded
        
    
    return energy + (deadline_penalty * penalty_factor)

# Cooling schedule for Simulated Annealing (reduces probability of accepting worse solutions)
def cooling_schedule(iteration, max_iterations):
    return max(0.01, min(1, 1 - (iteration / max_iterations)))

# Perform Simulated Annealing to explore nearby solutions
def simulated_annealing_step(particle):
    new_particle = particle.copy()
    # Randomly select two task-resource pairs
    task1, resource1 = random.choice(new_particle)
    task2, resource2 = random.choice(new_particle)
    # Ensure that task1 and task2 are not the same to avoid swapping the same task
    while task1.id == task2.id:
        task2, resource2 = random.choice(new_particle)


    # Remove the selected pairs from the new particle
    # Do this by comparing task.id and resource.id
    new_particle = [(t, r) for t, r in new_particle if not (t.id == task1.id and r.id == resource1.id)]
    new_particle = [(t, r) for t, r in new_particle if not (t.id == task2.id and r.id == resource2.id)]
    
    # Swap resources between the two tasks
    new_particle.append((task1, resource2))
    new_particle.append((task2, resource1))
    
    return new_particle

# PSO-SA Hybrid Optimization
def pso_sa_optimization(tasks, resources, num_particles, max_iterations):
    particles = initialize_particles(tasks, resources, num_particles)
    best_particle = None
    best_fitness = float('inf')

    for iteration in range(max_iterations):
        if True:
            print(f'iteration {iteration}')
        for particle in particles:
            fitness = calculate_fitness(particle)
            
            # Update best solution found
            if fitness < best_fitness:
                best_fitness = fitness
                best_particle = particle

            # Simulated Annealing refinement
            if random.random() < cooling_schedule(iteration, max_iterations):
                particle = simulated_annealing_step(particle)
    
    return best_particle

def pso():
    # Create task and resource objects
    tasks_np = np.load('./Comparesion/dataset/output/tasks.npy')
    resources_np = np.load('./Comparesion/dataset/output/resources.npy')

    tasks = []
    resources = []

    for i in range(tasks_np.shape[0]):
        temp_task = Task(id=int(tasks_np[i,0] - 1),computation_cost=tasks_np[i,1],deadline=tasks_np[i,3],input_size=tasks_np[i,5],output_size=tasks_np[i,6])
        tasks.append(temp_task)

    for i in range(resources_np.shape[0]):
        temp_resource = Resource(id=int(resources_np[i,0]),processing_speed=resources_np[i,2]
                                ,energy_efficiency=resources_np[i,3],type=resources_np[i,5])
        resources.append(temp_resource)

    # Run PSO-SA optimization
    best_schedule = pso_sa_optimization(tasks, resources, num_particles=30, max_iterations=100)

    results = []
    # Display the best schedule
    for task, resource in best_schedule:
        energy = resource.calculate_energy_consumption(task)
        exec_time = resource.calculate_execution_time(task)
        results.append((task.id,resource.id,exec_time,energy))
        #print(f"Task {task.id} -> Resource {resource.id} - Execution Time: {exec_time:.2f}, Energy: {energy:.2f}")

    results = np.array(results)
    np.save('./Comparesion/Algorithms/results/PSO-results.npy',results)


pso()