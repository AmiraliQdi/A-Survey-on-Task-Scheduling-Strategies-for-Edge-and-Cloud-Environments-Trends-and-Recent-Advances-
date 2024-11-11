import numpy as np


pso = np.load('./Comparesion/Algorithms/results/PSO-results.npy')
thems = np.load('./Comparesion/Algorithms/results/thems-results.npy')
whale = np.load('./Comparesion/Algorithms/results/whale-results.npy')
nsga = np.load('./Comparesion/Algorithms/results/NSGAII-results.npy')
drl = np.load('./Comparesion/Algorithms/results/drl-results.npy')

pso_time = np.mean(pso[:,2])
pso_energy = np.mean(pso[:,3])

print(f'PSO | time: {pso_time} / Energy: {pso_energy}')

thems_time = np.mean(thems[:,2])
thems_energy = np.mean(thems[:,3])

print(f'thems | time: {thems_time} / Energy: {thems_energy}')

whale_time = np.mean(whale[:,2])
whale_energy = np.mean(whale[:,3])

print(f'whale | time: {whale_time} / Energy: {whale_energy}')

nsga_time = np.mean(nsga[:,2])
nsga_energy = np.mean(nsga[:,3])

print(f'nsga | time: {nsga_time} / Energy: {nsga_energy}')

drl_time = np.mean(drl[:,2])
drl_energy = np.mean(drl[:,3])

print(f'drl | time: {drl_time} / Energy: {drl_energy}')

