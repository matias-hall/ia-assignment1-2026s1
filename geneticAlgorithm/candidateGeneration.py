import random

random.seed(2009)

# generate N candidate solutions
def generateCandidates(tasks, employees, N, flawed=False):
    candidates = []
    while len(candidates) < N:
        tasksN = tasks.copy()
        random.shuffle(tasksN)

        # local tracking for candidates
        remaining_hours = {emp.ID: emp.availableHours for emp in employees}
        task_counts = {emp.ID: 0 for emp in employees}

        assignments = []

        for task in tasksN:
            if flawed == True:
                availableEmployees = [
                    emp for emp in employees
                ]
            else:
                availableEmployees = [
                    emp for emp in employees
                    if task_counts[emp.ID] < 4
                    and task.requiredSkill in emp.skills
                    and remaining_hours[emp.ID] >= task.estTime
                    and emp.skillLevel >= task.difficulty
                ]

            if availableEmployees:
                assignedEmployee = random.choice(availableEmployees)
                task_counts[assignedEmployee.ID] += 1

                time_spent = assignedEmployee.availableHours - remaining_hours[assignedEmployee.ID]
                remaining_hours[assignedEmployee.ID] -= task.estTime

                assignments.append((task, assignedEmployee, time_spent))

        if len(assignments) == len(tasks):
            candidates.append(assignments)

    #printPairs(candidates)

    for i in range(len(candidates)):
        candidates[i] = sortTasks(candidates[i])


    for i in range(len(candidates)):
        candidates[i] = update_time_spent(candidates[i], employees)
    
    #printPairs(candidates)

    #for candidate in candidates:
        #print(calculateTotalPenalty(candidate))

    return candidates

def calculateDeadlinePenalty(candidate):
    penalty = 0
    for task, employee, timeSpent in candidate:
        if timeSpent > task.deadline:
            penalty += timeSpent - task.deadline
    return penalty

def calculateTotalPenalty(candidate):

    # overload penalty
    overloadPenalty = 0
    employeeTotalTime = {}
    for task, employee, timeSpent in candidate:
        if employee.ID not in employeeTotalTime:
            employeeTotalTime[employee.ID] = (employee, 0)
        emp, total = employeeTotalTime[employee.ID]
        employeeTotalTime[employee.ID] = (emp, total + task.estTime)
    
    for empID, (employee, totalTime) in employeeTotalTime.items():
        if totalTime > employee.availableHours:
            overloadPenalty += 0.2
    
    # skill mismatch penalty
    skillMismatchPenalty = 0
    for task, employee, timeSpent in candidate:
        if task.requiredSkill not in employee.skills:
            skillMismatchPenalty += 0.2

    # difficulty violation penalty
    difficultyViolationPenalty = 0
    for task, employee, timeSpent in candidate:
        if employee.skillLevel < task.difficulty:
            difficultyViolationPenalty += 0.2

    # deadline violation penalty
    deadlineViolationPenalty = 0
    for task, employee, timeSpent in candidate:
        if (timeSpent + task.estTime) > task.deadline:
            deadlineViolationPenalty += timeSpent + task.estTime - task.deadline
    deadlineViolationPenalty = deadlineViolationPenalty * 0.2  # weight deadline penalty more heavily

    # unique assignment violation penalty
    uniqueAssignmentViolationPenalty = 0
    seen_tasks = set()
    for task, employee, timeSpent in candidate:
        if task.ID in seen_tasks:
            uniqueAssignmentViolationPenalty += 0.2  # duplicate assignment
        else:
            seen_tasks.add(task.ID)

    penalty = overloadPenalty + skillMismatchPenalty + difficultyViolationPenalty + deadlineViolationPenalty + uniqueAssignmentViolationPenalty

    # avoiding floating point errors
    penalty = int(penalty * 10) / 10
    
    return penalty


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

def printPairs(candidates):
    for n in range(len(candidates)):
        print(f"Candidate {n}:")
        for pair in range(len(candidates[n])):
            print(candidates[n][pair])

def update_time_spent(candidate, employees):
    # creating a local copy of employee hours
    emp_hours = {emp.ID: emp.availableHours for emp in employees}
    spent_so_far = {emp.ID: 0 for emp in employees}
    updated_assignments = []
    for assignment in candidate:
        if not (isinstance(assignment, tuple) and len(assignment) == 3):
            continue
        task, employee, _ = assignment
        time_spent = spent_so_far[employee.ID]
        updated_assignments.append((task, employee, time_spent))
        spent_so_far[employee.ID] += task.estTime
    return updated_assignments

def sortTasks(candidate):
    return sorted(candidate, key=lambda x: (x[0].estTime, x[0].deadline))