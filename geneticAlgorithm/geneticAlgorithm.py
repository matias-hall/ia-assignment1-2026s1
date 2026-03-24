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
                #print(candidates[n][len(candidates[n])-1])
                #print(assignedEmployee.remainingHours)

                
            else:
                print(f"No available employee for task {task.ID}")

            #save this data?

    for n in range(N - 1, -1, -1):
        if len(candidates[n]) < len(tasks):
            #print(f"Candidate {n} is invalid: not all tasks assigned")
            candidates.pop(n)
        else:
            print(f"Candidate {n} is valid")
            #print(candidates[n])


    
    
    

        
                

    return candidates

# represent each solution as a vector where each element indicates the employee assigned to a specific task

# use crossover and mutation to evolve the solution population

# evaluate solutions based on penalties for any constraint violations