import random

t = 10  # number of tasks, rows in pheromone array
e = 5 # number of employees, cols in pheromone array

# for skill level eg A, B, C, only an individual task
def skill_mismatch_penalty(taskSkill, empSkills):
    penalty = 0
    if taskSkill not in empSkills:
        penalty = 10

    return penalty

#overload for one specific employee
def employee_overload(emp_id, emps, solution, tasks):
    totalTime = 0
    overload = 0
    for task in range(t):
        if solution[task] == emp_id:
            totalTime += tasks[task].estTime
    # work out hours overworked for each employee
    if(totalTime > emps[emp_id].availableHours):
        overload = overload + (totalTime - emps[emp_id].availableHours)

    return overload

# deadline penalty function as defined in assignment sheet
def deadline_penalty(tasks, emp_id, solution):
    deadline = []
    finishTime = 0
    penalty = 0

    for task in range(t):
        if solution[task] == emp_id:
            deadline.append([task, tasks[task].estTime, tasks[task].deadline])
    
    deadline = sorted(deadline, key = lambda x: x[1])
    
    for task in deadline:
        finishTime += task[1]
        penalty = penalty + max(finishTime - task[2], 0)

    return penalty

def calculate_fitness(solution, tasks, employees, violations):
    """
    Fitness = minimise cost function
    Best fitness = 0
    """
    
    cost = 0 # cost = fitness

    # employee penalties overload and deadline, done seperate to tasks (as to get all of an employees assigned tasks)
    for emp_id in range(e):
        overload = employee_overload(emp_id, employees, solution, tasks)
        if overload != 0:
            violations += 1
        deadlineViol = deadline_penalty(tasks, emp_id, solution)
        if deadlineViol != 0:
            violations += 1

        cost += 0.2 * overload + 0.2 * deadlineViol


    # for each task, get penalties of skill and difficulty
    for task in range(t):
        
        uniqAssignViol = 0 # automatically assigned in solution
        diffViol = 0

        skillMismatch = skill_mismatch_penalty(tasks[task].requiredSkill, employees[solution[task]].skills)
        if skillMismatch != 0:
            violations += 1

        # difficulty level
        if tasks[task].difficulty > employees[solution[task]].skillLevel:
            diffViol += 10
            violations += 1

        # cost function to minimise
        cost += 0.2 * skillMismatch + 0.2 * diffViol + 0.2 * uniqAssignViol
        

    return cost, violations

def construct_solution(pheromone):
    """
    Build one solution row by row.
    For each row, choose a column based on pheromone values.
    """
    solution = [] # each row (out of 10 indices) is a task and each column is an employee assignment (employee ID)

    for row in range(t):
        total_pheromone = sum(pheromone[row])

        # If pheromone is zero, choose a random column
        if total_pheromone == 0:
            chosen_col = random.randint(0, e - 1)
            solution.append(chosen_col)
            continue

        # Roulette wheel selection
        r = random.uniform(0, total_pheromone)
        cumulative = 0
        chosen_col = 0

        # use cumulative probability
        for col in range(e):
            cumulative += pheromone[row][col]
            if cumulative >= r:
                chosen_col = col
                break

        solution.append(chosen_col)
        
    return solution


def update_pheromone(pheromone, solutions, fitnesses, evaporation_rate, Q):
    """
    Update pheromone in two steps:
    1. Evaporation: reduce old pheromone
    2. Deposit: add new pheromone from good solutions
    """

    # Step 1: Evaporation
    for i in range(t):
        for c in range(e):
            pheromone[i][c] *= (1 - evaporation_rate)

    # Step 2: Deposit
    for solution, fitness in zip(solutions, fitnesses):
        # Better fitness gives larger pheromone deposit. highest reward is 1 (if Q = 1), for a minimisation function
        deposit_amount = Q / (1 + fitness)

        for row, col in enumerate(solution):
            pheromone[row][col] += deposit_amount

def print_board(solution):
    """
    Show the final board.
    E = employee assigned to task (row)
    . = empty
    """
    for row in range(t):
        line = []
        for col in range(e):
            if solution[row] == col:
                line.append("E")
            else:
                line.append(".")
        print(" ".join(line))

def ant_colony_optimization(num_ants, evaporation_rate, Q, max_iterations, tasks, employees):
    """
    Main ACO process:
    - initialize pheromone
    - let ants build solutions
    - evaluate solutions
    - update pheromone
    - keep the best solution
    """

    # Initial pheromone matrix (2D array)
    pheromone = [[1.0 for _ in range(e)] for _ in range(t)]
    
    best_solution = None
    best_fitness = float("inf")
    violations = 0

    for iteration in range(max_iterations):
        solutions = []
        fitnesses = []

        # Each ant builds one solution
        for _ in range(num_ants):
            solution = construct_solution(pheromone)
            fitness, v = calculate_fitness(solution, tasks, employees, 0)

            violations += v
            solutions.append(solution)
            fitnesses.append(fitness)

            # Save the best solution found so far
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = solution

        # Update pheromone after all ants finish
        update_pheromone(pheromone, solutions, fitnesses, evaporation_rate, Q)

        print(f"Iteration {iteration + 1}: Best fitness so far = {best_fitness:.1f} Num of Violations: {violations}")

        # Stop early if perfect solution is found
        if best_fitness == 0:
            break


    print("\nBest solution:", best_solution)
    print("Best fitness:", best_fitness)
    print("\nGraph:")
    print_board(best_solution)

    return best_solution, best_fitness
