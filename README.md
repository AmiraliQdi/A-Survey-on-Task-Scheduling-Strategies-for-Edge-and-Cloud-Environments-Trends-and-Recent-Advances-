---

# A Survey on Task Scheduling Strategies for Edge and Cloud Environments: Trends and Recent Advances

This repository contains the code, data, and findings for the survey titled **"A Survey on Task Scheduling Strategies for Edge and Cloud Environments: Trends and Recent Advances."** In this study, we analyze and compare five prominent algorithms used for task scheduling across edge devices and cloud environments, focusing on their optimization goals, strategies, and performance.

## Algorithms Analyzed

### 1. THEMES
   **Description**: THEMES is a heuristic-based approach to task scheduling that uses a greedy search to find feasible scheduling solutions. While effective for simpler tasks, this approach may struggle in complex and dynamic environments.

   - **Optimization Goals**: Minimizes execution time and energy consumption, combined into a single scalar objective. Resource capacity is also considered.
   - **Advantages**: Simple and efficient for straightforward tasks.
   - **Disadvantages**: Limited in handling complex dependencies and dynamic workloads.

### 2. Deep Reinforcement Learning (DRL)
   **Description**: DRL applies reinforcement learning to improve scheduling for complex and dynamic environments. This approach adapts and improves over time, though debugging can be challenging.

   - **Optimization Goals**: Capable of handling multiple objectives, including task criticality, dependencies (predecessors and successors), deadlines, and resource capacities.
   - **Advantages**: Flexible and able to accommodate complex, competing objectives.
   - **Disadvantages**: Computationally intensive and may be unreliable in certain scenarios.

### 3. Hybrid PSO-SA (Particle Swarm Optimization and Simulated Annealing)
   Based on the paper **"An Energy-efficient and Deadline-aware Workflow Scheduling Algorithm in the Fog and Cloud Environment"** by **N. Khaledian, K. Khamforoosh, and R. Akraminejad**, this algorithm combines PSO and SA to balance exploration and exploitation in scheduling.

   - **Optimization Goals**: Reduces energy consumption, meets deadlines, and enhances overall makespan.
   - **Task and Resource Attributes**: Considers computation cost, deadline constraints, resource processing speed, and energy efficiency.
   - **Advantages**: Balances energy efficiency with deadline adherence.
   - **Disadvantages**: May require careful tuning to optimize for specific task environments.

### 4. NSGA-II (Non-dominated Sorting Genetic Algorithm II)
   **Description**: NSGA-II is a multi-objective optimization algorithm for task scheduling, particularly suitable for environments with fog and cloud nodes.

   - **Optimization Goals**: Optimizes processing time, energy consumption, and task deadlines.
   - **Task and Resource Attributes**: Considers task processing time, baseline energy, deadline, and resource-specific attributes like capacity, efficiency, execution speed, and idle power.
   - **Advantages**: Strong in multi-objective optimization with effective load balancing.
   - **Disadvantages**: Computational complexity increases with more tasks and resource constraints.

### 5. Whale Optimization Algorithm (WOA)
   Based on the paper **"A Cost-Efficient IoT Service Placement Approach using Whale Optimization Algorithm in Fog Computing Environment"** by **M. Ghobaei-Arani and A. Shahidinejad**, WOA is a metaheuristic algorithm tailored to IoT service placement in fog environments.

   - **Optimization Goals**: Reduces deployment costs, optimizes energy usage, and ensures quality of service (QoS).
   - **Task and Resource Attributes**: Includes computational demand, QoS requirements, processing capacity, energy efficiency, and resource availability.
   - **Advantages**: Efficient global search for cost-effective placements.
   - **Disadvantages**: Sensitive to parameter tuning and may require higher computational resources.

## Dataset

The dataset used in this survey includes:

1. **Resources**: Representing active simulated resources available to the edge network with the following attributes:
   - **Processing Speed**
   - **Energy Efficiency**
   - **Capacity**
   - **Type** (e.g., IoT device, MEC, or cloud resource)

2. **Tasks**: Represent the smallest schedulable unit in the network with attributes:
   - **Computation Cost**
   - **Deadline**
   - **Input Size** (for estimating communication cost during uploads)
   - **Output Size** (for estimating communication cost during downloads)

## Environment Setup

To ensure consistency, the same dataset of resources and tasks was used to train and test all algorithms. Additionally, **communication cost** was incorporated into the environment:
   - If a task originates from an IoT device, additional time and energy costs are added for uploading it to another device, particularly for larger tasks offloaded to clouds or MECs.

## Performance Metrics

Each algorithm's performance was evaluated based on:
1. **Execution Time**: Total time required to complete all tasks.
2. **Energy Consumption**: Energy utilized across all resources, with penalties for inefficient allocations.
3. **Deadline Adherence**: Compliance with task deadlines, ensuring timely task completions.
4. **Communication Cost**: The time and energy required for task offloading, especially when an IoT device initiates the task.

## Repository Structure

- **/data**: Contains the dataset files, including resource and task characteristics.
- **/src**: Contains implementations for each algorithm.
- **/results**: Performance results and analysis for each algorithm on the standardized dataset.
- **README.md**: Overview of the project and instructions for usage.

## How to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AmiraliQdi/Task-Scheduling-Survey.git
   cd Task-Scheduling-Survey
   ```

2. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Each Algorithm**:
   Each algorithm script can be executed individually from the `/Algorithms/algorithm-name/main.py` directory. Results will be saved in `/results` as numpy arrays for now that can be compared in `/results/test-results.py`.

4. **Analyze Results**:
   Results are presented in both raw data and summarized metrics to compare execution time, energy consumption, and deadline adherence.

---
