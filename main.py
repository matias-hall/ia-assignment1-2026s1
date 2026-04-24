# import modules from subfolders and benchmarking.py
import classes
import functions
import random
import benchmarking
import geneticAlgorithm.geneticAlgorithm as gA
# import particleSwarmOptimisation.particleSwarmOptimisation as pSO
import antColonyOptimisation.antColonyOptimisation as aCO
from data import get_data

random.seed(2009)

tasks, employees = get_data('taskdata.csv', 'employeedata.csv')

# benchmarking functions

# run algorithms

N = 5

# start benchmark
gA.geneticAlgorithm(tasks, employees, N)
# stop benchmark

# result, score = pSO.particle_swarm_optimisation(tasks, employees)
# print(f"{result} ({score})")

# stop benchmark
