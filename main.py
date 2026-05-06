# import modules from subfolders and benchmarking.py
import classes
import functions
import random
import benchmarking
import time
import geneticAlgorithm.geneticAlgorithm as gA
import particleSwarmOptimisation.particleSwarmOptimisation as pSO
import antColonyOptimisation.antColonyOptimisation as aCO
from data import get_data

import argparse

tasks, employees = get_data('taskdata.csv', 'employeedata.csv')

# benchmarking functions

# run algorithms

N = 5

# start benchmark
def benchmark_ga(tasks, employees):
    start = time.perf_counter()

    maxGenerations = 100
    crossoverRate = 0.7
    mutationRate = 0.01

    gA.geneticAlgorithm(tasks, employees, N, maxGenerations, crossoverRate, mutationRate)
    #gA.evaluateGA(tasks, employees, N)
    
    end = time.perf_counter()

    runtime = end - start
    print("Total runtime is: ", runtime)

def benchmark_pso(tasks, employees):
    start = time.perf_counter()
    result, score = pSO.particle_swarm_optimisation(tasks, employees, w=0.82, c1=1.4, c2=1.1, max_iterations=500)
    print(f"{result} ({score})")
    # Print results
    end = time.perf_counter()

    runtime = end - start
    print("Total runtime is: ", runtime)

def benchmark_aco(tasks, employees):
    start = time.perf_counter()
    ants = 30 
    Q = 1
    maxIt = 500
    evapRate = 0.3
    aCO.ant_colony_optimization(ants, evapRate, Q, maxIt, tasks, employees) 
    end = time.perf_counter()

    runtime = end - start
    print("Total runtime is: ", runtime)
    # prints results inside the function
# stop benchmark


# stop benchmark

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='Task Assigner',
            description='Uses three different metaheuristic algorithms to assign tasks to employees')
    parser.add_argument('algorithm', default='all', choices=['all', 'ga', 'pso', 'aco'], nargs='?')
    parser.add_argument('task_data')
    parser.add_argument('employee_data')
    args = parser.parse_args()

    tasks, employees = get_data(args.task_data, args.employee_data)
    if args.algorithm == 'all':
        benchmark_ga(tasks, employees)
        benchmark_pso(tasks, employees)
        benchmark_aco(tasks, employees)
    elif args.algorithm == 'ga':
        benchmark_ga(tasks, employees)
    elif args.algorithm == 'pso':
        benchmark_pso(tasks, employees)
    elif args.algorithm == 'aco':
        benchmark_aco(tasks, employees)
