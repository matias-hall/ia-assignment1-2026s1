#! implement genetic algorithm
import random

random.seed(2009)

# generate N candidate solutions
def geneticAlgorithm(tasks, employees, N):

    pairings = [[] for _ in range(N)]

    #! assign each person no more than 4 tasks?

    for n in range(N):
        order = ["T1","T2","T3","T4","T5","T6","T7","T8","T9","T10"]

        random.shuffle(order)

                #for each task, assign a random employee up to a maximum for 4 tasks per employee
        employeeTaskCounts = {employee.ID: 0 for employee in employees}
        for task in order:
            availableEmployees = [employee for employee in employees if employeeTaskCounts[employee.ID] < 4]
            if availableEmployees:
                assignedEmployee = random.choice(availableEmployees)
                employeeTaskCounts[assignedEmployee.ID] += 1

            #save this data?
            pairings[n].append((task, assignedEmployee.ID))


        # convert pairings to task and employee objects for evaluation
        pairings[n] = [(next(task for task in tasks if task.ID == taskID), next(employee for employee in employees if employee.ID == empID)) for taskID, empID in pairings[n]]

        # test the validity of the pairings and calculate penalties for any constraint violations
        for pair in range(len(pairings[n])):
            print(pairings[n][pair])

        #! use skill matching
                

    return pairings

# represent each solution as a vector where each element indicates the employee assigned to a specific task

# use crossover and mutation to evolve the solution population

# evaluate solutions based on penalties for any constraint violations