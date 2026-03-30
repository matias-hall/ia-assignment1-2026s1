#! implement genetic algorithm
import random

random.seed(2009)

# generate N candidate solutions
def geneticAlgorithm(tasks, employees, N):

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
            
                candidates[n].append((task, assignedEmployee))

            else:
                print(f"No available employee for task {task.ID}")

    for n in range(N - 1, -1, -1):
        if len(candidates[n]) < len(tasks):
            #print(f"Candidate {n} is invalid: not all tasks assigned")
            candidates.pop(n)
        else:
            print(f"Candidate {n} is valid")


    #checkConstraints(candidates, employees) # verifying the constraints of the generated candidates

    
    for n in range(len(candidates)):
        print(candidates[n])
        print(deadlinePenalty(candidates[n]))
    
    
    

        
                

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
    for task, employee in candidate:
        if (employee.availableHours - employee.remainingHours) > task.deadline:
            print(f"Deadline violation: Task {task.ID} is overdue")
            deadlinePenalty += (employee.availableHours - employee.remainingHours) + task.estTime - task.deadline

    return deadlinePenalty