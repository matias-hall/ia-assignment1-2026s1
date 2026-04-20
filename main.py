# import modules from subfolders and benchmarking.py
import classes
import functions
import random
import benchmarking
import geneticAlgorithm.geneticAlgorithm as gA
import particleSwarmOptimisation.particleSwarmOptimisation as pSO
import antColonyOptimisation.antColonyOptimisation as aCO

random.seed(2009)

# read data

taskdata = """
T1,4,3,8,A
T2,6,5,12,B
T3,2,2,6,A
T4,5,4,10,C
T5,3,1,7,A
T6,8,6,15,B
T7,4,3,9,C
T8,7,5,14,B
T9,2,2,5,A
T10,6,4,11,C
"""

employeeData = """
E1,10,4,AC
E2,12,6,ABC
E3,8,3,A
E4,15,7,BC
E5,9,5,AC
"""

tasks = []  # list of tasks
employees = []  # list of employees

for line in taskdata.strip().split("\n"):
    ID, estTime, difficulty, deadline, requiredSkill = line.split(",")
    task = classes.task(ID, int(estTime), int(difficulty), int(deadline), requiredSkill)
    tasks.append(task)  # add task to the list

for line in employeeData.strip().split("\n"):
    ID, availableHours, skillLevel, skills = line.split(",")
    employee = classes.employee(ID, int(availableHours), int(availableHours), int(skillLevel), list(skills))  # setting remainingHours to availableHours
    employees.append(employee)  # add employee to the list

# benchmarking functions

# run algorithms

N = 20

# start benchmark
gA.geneticAlgorithm(tasks, employees, N)

result, score = pSO.particle_swarm_optimisation(tasks, employees)
print(f"{result} ({score})")

# stop benchmark
