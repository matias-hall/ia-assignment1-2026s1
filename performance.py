# import modules from subfolders and benchmarking.py
import classes
import functions
import random
import benchmarking
import particleSwarmOptimisation.particleSwarmOptimisation as pSO
from data import get_data

import matplotlib.pyplot as plt
import numpy as np

import time

tasks, employees = get_data('taskdata.csv', 'employeedata.csv')

trials = 50

# Collects the score and best candidate at each iteration
class DataCollector():
    def __init__(self):
        self.data = []
    def collect(self, *data):
        self.data.append(data)

# Collects the time it takes to reach each iteration from the start
class Profiler():
    def __init__(self):
        self.start = time.time()
        self.data = []
    def collect(self, *data):
        self.data.append(time.time() - self.start)

# Collects the number of broken constraints at each iteration
class ConstraintChecker():
    def __init__(self, tasks, employees):
        self.start = time.time()
        self.data = []
        self.tasks = tasks
        self.employees = employees
    def collect(self, *data):
        assignment = data[0]
        overload = 0
        for employee_index in range(len(self.employees)):
            # + 1 since employee ids are 1-indexed
            assigned_tasks = [i for i, x in enumerate(assignment) if x == employee_index + 1]
            total_time = 0
            for task_index in assigned_tasks:
                total_time += self.tasks[task_index].estTime

            overload += 1 if total_time > self.employees[employee_index].availableHours else 0

        skill_mismatch = 0
        for task_index, employee_id in enumerate(assignment):
            required_skill = self.tasks[task_index].requiredSkill
            # - 1 since employee ids are 1-indexed
            skillset = self.employees[employee_id - 1].skills

            skill_mismatch += 1 if required_skill not in skillset else 0

        difficulty_violation = 0
        for task_index, employee_id in enumerate(assignment):
            difficulty = self.tasks[task_index].difficulty
            skill_level = self.employees[employee_id - 1].skillLevel

            difficulty_violation += 1 if difficulty > skill_level else 0

        deadline_violation = 0
        for employee_index in range(len(self.employees)):
            # + 1 since employee ids are 1-indexed
            assigned_tasks = [self.tasks[i] for i, x in enumerate(assignment) if x == employee_index + 1]

            assigned_tasks.sort(key=lambda x: x.estTime)
            time_taken = 0
            for task in assigned_tasks:
                time_taken += task.estTime
                deadline_violation += 1 if time_taken > task.deadline else 0

        total =  overload + skill_mismatch + difficulty_violation + deadline_violation
        self.data.append(total)

def solution_quality(tasks, employees):
    fig, ax = plt.subplots()
    ax.set_title(f'Solution Quality (trials: {trials})')
    ax.set_xlabel('Iteration number')
    ax.set_ylabel('Penalty (lower is better)')
    Y_total = np.zeros(shape=(500))
    X = np.array(range(500))

    for i in range(trials):
        collector = DataCollector()
        result, score = pSO.particle_swarm_optimisation(tasks, employees, iteration_hook=collector.collect, max_iterations=500, w=0.82, c1=1.4, c2=1.1)
        Y = np.array(list(map(lambda x: x[1], collector.data)))
        Y = np.append(Y, np.full((500-Y.size), Y[-1]))
        Y_total += Y
        ax.plot(X, Y, 'k-', alpha=0.5)
    Y_total /= trials
    ax.plot(X, Y_total, 'r-', label='Average')
    ax.legend()
    plt.savefig('quality.png')
    # Print results
    # Stop timer

def computational_efficiency(tasks, employees):
    fig, ax = plt.subplots()
    ax.set_title(f'Computation Efficiency (trials: {trials})')
    ax.set_xlabel('Iteration number')
    ax.set_ylabel('Runtime (seconds)')
    Y_total = np.zeros(shape=(500))
    X = np.array(range(500))

    for i in range(trials):
        profiler = Profiler()
        result, score = pSO.particle_swarm_optimisation(tasks, employees, iteration_hook=profiler.collect, max_iterations=500, w=0.82, c1=1.4, c2=1.1)
        Y = np.array(profiler.data)
        Y = np.append(Y, np.full((500-Y.size), Y[-1]))
        Y_total += Y
        ax.plot(X, Y, 'k-', alpha=0.5)
    Y_total /= trials
    ax.plot(X, Y_total, 'r-', label='Average')
    ax.legend()
    plt.savefig('efficiency.png')

def constraint_satisfaction(tasks, employees):
    fig, ax = plt.subplots()
    ax.set_title(f'Constraint Satisfaction (trials: {trials})')
    ax.set_xlabel('Iteration number')
    ax.set_ylabel('Broken constraints (lower is better)')
    Y_total = np.zeros(shape=(500))
    X = np.array(range(500))

    for i in range(trials):
        profiler = ConstraintChecker(tasks, employees)
        result, score = pSO.particle_swarm_optimisation(tasks, employees, iteration_hook=profiler.collect, max_iterations=500, w=0.82, c1=1.4, c2=1.1)
        Y = np.array(profiler.data)
        Y = np.append(Y, np.full((500-Y.size), Y[-1]))
        Y_total += Y
        ax.plot(X, Y, 'k-', alpha=0.5)
    Y_total /= trials
    ax.plot(X, Y_total, 'r-', label='Average')
    ax.legend()
    plt.savefig('constraints.png')

def final_constraints(tasks, employees):
    fig, ax = plt.subplots()
    ax.set_title(f'Constraint Satisfaction (trials: {trials})')
    ax.set_xlabel('Broken constraints (lower is better)')
    ax.set_ylabel('Count')
    X = np.array(range(trials))

    for i in range(trials):
        profiler = ConstraintChecker(tasks, employees)
        result, score = pSO.particle_swarm_optimisation(tasks, employees, iteration_hook=profiler.collect, max_iterations=500, w=0.82, c1=1.4, c2=1.1)
        X[i] = profiler.data[-1]
    elements, count = np.unique(X, return_counts=True)
    ax.bar(elements, count)
    ax.set_xticks(elements)
    plt.savefig('final_constraints.png')

# Generate all the graphs
solution_quality(tasks, employees)
computational_efficiency(tasks, employees)
constraint_satisfaction(tasks, employees)
final_constraints(tasks, employees)
