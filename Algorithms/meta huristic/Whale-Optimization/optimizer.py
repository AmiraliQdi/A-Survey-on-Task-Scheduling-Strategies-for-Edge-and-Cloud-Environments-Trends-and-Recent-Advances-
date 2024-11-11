import numpy as np
from objects import calc_time_energy

class WhaleOptimizationScheduling:
    def __init__(self, tasks, resources, num_whales, max_iter):
        self.tasks = tasks
        self.resources = resources
        self.num_tasks = len(tasks)
        self.num_resources = len(resources)
        self.num_whales = num_whales
        self.max_iter = max_iter

        self.whales = np.random.randint(0, self.num_resources, size=(self.num_whales, self.num_tasks))

        self.best_whale = np.zeros(self.num_tasks, dtype=int)
        self.best_score = float('inf')

    def optimize(self):
        for t in range(self.max_iter):
            if t % 50 == 0:
                print('iteration',t)
            for i in range(self.num_whales):
                fitness = objective_function(self.whales[i], self.tasks, self.resources)
                if fitness < self.best_score:
                    self.best_score = fitness
                    self.best_whale = self.whales[i].copy()

            a = 2 - 2 * t / self.max_iter

            for i in range(self.num_whales):
                r = np.random.uniform(0, 1, self.num_tasks)  # Random vector

                if np.random.rand() < 0.5:
                    A = 2 * a * r - a
                    D = np.abs(A * self.best_whale - self.whales[i])
                    self.whales[i] = np.clip(self.best_whale - A * D, 0, self.num_resources - 1).astype(
                        int)
                else:
                    b = 1
                    l = np.random.uniform(-1, 1)
                    D_prime = np.abs(self.best_whale - self.whales[i])
                    self.whales[i] = np.clip(D_prime * np.exp(b * l) * np.cos(2 * np.pi * l) + self.best_whale,
                                             0, self.num_resources - 1).astype(int)

            # print(f"Iteration {t + 1}, Best Fitness: {self.best_score}")

        return self.best_whale, self.best_score


def objective_function(whale_position, tasks, resources, lambda_penalty=100):
    total_energy = 0
    total_time = 0
    penalty_for_missed_deadlines = 0

    for task_idx, resource_idx in enumerate(whale_position):
        task = tasks[task_idx]
        resource = resources[resource_idx]
        execution_time = resource.execution_time(task)
        energy_used = (task.computation_cost // resource.processing_speed + 1) * resource.energy_efficiency
        t, e = calc_time_energy(execution_time, energy_used, resource.type,task.input_size,task.output_size)

        if resource.can_execute(e, task):
            total_energy += e
            total_time += t
            resource.execute(e)
            if t > task.deadline:
                penalty = lambda_penalty * (execution_time - task.deadline)
                penalty_for_missed_deadlines += penalty
        else:
            penalty_for_missed_deadlines += lambda_penalty * 100

    total_cost = total_energy + total_time + penalty_for_missed_deadlines

    for _, resource_idx in enumerate(whale_position):
        resources[resource_idx].reset()
    return total_cost
