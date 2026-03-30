#! implement genetic algorithm
import random

random.seed(2009)

def geneticAlgorithm(tasks, employees, N):
    candidates = generateCandidates(tasks, employees, N)
    #! add crossover and mutation functions here to evolve the candidate solutions

# generate N candidate solutions
def generateCandidates(tasks, employees, N):

    candidates = [[] for _ in range(N)]


    for n in range(N):
        tasksN = tasks.copy()
        random.shuffle(tasksN)

        for employee in employees:
            employee.remainingHours = employee.availableHours

            
        employeeTaskCounts = {employee.ID: 0 for employee in employees}
        for task in tasksN:
            availableEmployees = [employee for employee in employees if employeeTaskCounts[employee.ID] < 4 and task.requiredSkill in employee.skills and employee.remainingHours >= task.estTime and employee.skillLevel >= task.difficulty]
            
            #! add sorting based on processing/deadline time?

            if availableEmployees:
                assignedEmployee = random.choice(availableEmployees)
                employeeTaskCounts[assignedEmployee.ID] += 1

                assignedEmployee.remainingHours -= task.estTime
                remainingHours = assignedEmployee.remainingHours

            
                candidates[n].append((task, assignedEmployee, remainingHours))

            """
            else:
                print(f"No available employee for task {task.ID}")
            """

    for n in range(N - 1, -1, -1):
        if len(candidates[n]) < len(tasks):
            #print(f"Candidate {n} is invalid: not all tasks assigned")
            candidates.pop(n)
        else:
            print(f"Candidate {n} is valid")


    #checkConstraints(candidates, employees) # verifying the constraints of the generated candidates


    for candidate in range(len(candidates)):
        candidates[candidate].append(deadlinePenalty(candidates[candidate]))  # appending the deadline penalty to each candidate

    printPairs(candidates)

                

    return candidates

# represent each solution as a vector where each element indicates the employee assigned to a specific task

# use crossover and mutation to evolve the solution population

# evaluate solutions based on penalties for any constraint violations

def checkConstraints(candidates, employees):
    for n in range(len(candidates)):
        employeeTime = {employee.ID: 0 for employee in employees}
        for pair in range(len(candidates[n])):
            if candidates[n][pair][1] is not None:
                assignedEmployee = candidates[n][pair][1]
                employeeTime[assignedEmployee.ID] += candidates[n][pair][0].estTime

        for employeeID, totalTime in employeeTime.items():
            if totalTime > next(employee.availableHours for employee in employees if employee.ID == employeeID):
                print(f"Constraint violation: Employee {employeeID} is overbooked with {totalTime} hours")
            else:
                print(f"Employee {employeeID} is within capacity with {totalTime} hours")

def deadlinePenalty(candidate):
    deadlinePenalty = 0
    for task, employee, remainingHours in candidate:
        if (employee.availableHours - remainingHours) > task.deadline:
            #print(f"Deadline violation: Task {task.ID} is overdue")
            deadlinePenalty += (employee.availableHours - remainingHours) - task.deadline
            #print(f"{employee.ID} has worked {employee.availableHours - remainingHours} hours on task {task.ID}, which exceeds the deadline of {task.deadline} hours")
    #print(deadlinePenalty)

    return deadlinePenalty

def printPairs(candidates):
    for n in range(len(candidates)):
        print(f"Candidate {n}:")
        for pair in range(len(candidates[n])):
            print(candidates[n][pair])