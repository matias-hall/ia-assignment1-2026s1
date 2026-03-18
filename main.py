# import modules from subfolders and benchmarking.py
from benchmarking import *
import classes

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

for line in taskdata.strip().split("\n"):
    ID, estTime, difficulty, deadline, requiredSkill = line.split(",")
    task = classes.task(ID, int(estTime), int(difficulty), int(deadline), requiredSkill)
    print(task)

for line in employeeData.strip().split("\n"):
    ID, availableHours, skillLevel, skills = line.split(",")
    employee = classes.employee(ID, int(availableHours), int(skillLevel), skills.split(","))
    # split skills into individual letters in a matrix
    print(employee)

# benchmarking functions

# run algorithms