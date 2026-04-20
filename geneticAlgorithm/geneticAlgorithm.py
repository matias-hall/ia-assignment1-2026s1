#! implement genetic algorithm
import random

random.seed(2009)

def geneticAlgorithm(tasks, employees, N):
    candidates = generateCandidates(tasks, employees, N)

    totalFitness = computeTotalFitness(candidates)
    
    generation = 0
    terminationCondition = False
    maxGenerations = 100
    mutationRate = 0.01

    while generation <= maxGenerations and terminationCondition == False:
        newPopulation = []
        while len(newPopulation) < len(candidates):
            parent1 = selectParent(candidates, totalFitness)
            parent2 = selectParent(candidates, totalFitness)
            if (random.random() < crossoverRate):  # crossover probability
                offspring1, offspring2 = crossover(parent1, parent2)
            else:
                offspring1, offspring2 = parent1, parent2  # no crossover, offspring are copies of parents
            offspring1 = mutate(offspring1, mutationRate)
            offspring2 = mutate(offspring2, mutationRate)

            offspring1 = EvaluateFitness(offspring1)
            offspring2 = EvaluateFitness(offspring2)

            newPopulation.append(offspring1)
            newPopulation.append(offspring2)

        candidates = newPopulation
        generation += 1
    
    bestCandidate = GetBestIndividual(candidates)
    return bestCandidate





    """

    for candidate in candidates:
        sortedCandidate = sorted(candidate[:-1], key=lambda x: x[0].ID)
        sortedCandidate.append(candidate[-1])  # append the deadline penalty at the end of the sorted candidate

    #! make T10 the second last element
        sortedCandidate.insert(-1, sortedCandidate.pop(sortedCandidate.index(next(pair for pair in sortedCandidate if pair[0].ID == "T10"))))  # move T10 to the

    print(sortedCandidate)  # sort tasks by ID, excluding the last element which is the deadline penalty

    solutionMatrix = []
    
    for task, employee, remainingHours in sortedCandidate[:-1]:  # exclude the deadline penalty at the end
        print(employee.ID[1:])
        ID = int(employee.ID[1:])
        solutionMatrix.append(ID)
    
    print(solutionMatrix)

    """

    #! add crossover and mutation functions here to evolve the candidate solutions

def crossover(parent1, parent2):
    pass

def mutate(candidate, mutationRate):
    for i in range(len(candidate) - 1):  # exclude the last element which is the deadline penalty
        if random.random() < mutationRate:
            
    pass

def computeTotalFitness(candidates):
    totalFitness = 0
    for candidate in candidates:
        totalFitness += candidate[10]
    return totalFitness

def selectParent(candidates, totalFitness):
    pick = random.uniform(0, totalFitness)
    current = 0
    for candidate in candidates:
        current += candidate[10]
        if current > pick:
            return candidate

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

    #printPairs(candidates)

                

    return candidates

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