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
def employee_overload(employee, emp_data, solution):
    totalTime = 0
    overload = 0
    for task in range(t):
        if solution[task] == employee:
            totalTime += task_data[task][0]
    # work out hours overworked for each employee
    if(totalTime > emp_data[employee][0]):
        overload = overload + (totalTime - emp_data[employee][0])

    return overload

# deadline penalty as described in assignment specifications
def deadline_penalty(task_data, emp_data, emp, solution):
    deadline = []
    finishTime = 0
    penalty = 0

    for task in range(t):
        if solution[task] == emp:
            deadline.append([task, task_data[task][0], task_data[task][2]])

    # sort tasks by ascending processing time
    deadline = sorted(deadline, key = lambda x: x[1])
    
    for task in deadline:
        finishTime += task[1]
        penalty = penalty + max(finishTime - task[2], 0)

    return penalty

def calculate_fitness(solution, task_data, emp_data):
    """
    Fitness = minimise cost function
    Best fitness = 0
    """
    
    cost = 0 # cost = fitness

    # employee penalties
    for emp in emp_data:
        overload = employee_overload(emp, emp_data, solution)
        deadlineViol = deadline_penalty(task_data, emp_data, emp, solution)

        cost += 0.2 * overload + 0.2 * deadlineViol


    # for each task, get fitness
    for task in range(t):
        
        uniqAssignViol = 0 # automatically assigned in solution
        diffViol = 0

        skillMismatch = skill_mismatch_penalty(task_data[task][3], emp_data[solution[task]][2])

        # difficulty level
        if task_data[task][1] > emp_data[solution[task]][1]:
            diffViol += 10

        # cost function to minimise
        cost += 0.2 * skillMismatch + 0.2 * diffViol + 0.2 * uniqAssignViol
        

    return cost


def construct_solution(pheromone):
    """
    Build one solution row by row. 
    For each row, choose a column based on pheromone values.
    Each row is a task and each column is an employee
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
        # Better fitness gives larger pheromone deposit
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


def ant_colony_optimization(num_ants, evaporation_rate, Q, max_iterations, task_data, emp_data):
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

    for iteration in range(max_iterations):
        solutions = []
        fitnesses = []

        # Each ant builds one solution
        for _ in range(num_ants):
            solution = construct_solution(pheromone)
            fitness = calculate_fitness(solution, task_data, emp_data)

            solutions.append(solution)
            fitnesses.append(fitness)

            # Save the best solution found so far
            if fitness < best_fitness:
                best_fitness = fitness
                best_solution = solution

        # Update pheromone after all ants finish
        update_pheromone(pheromone, solutions, fitnesses, evaporation_rate, Q)

        #print(f"Iteration {iteration + 1}: Best fitness so far = {best_fitness:.1f}")

        # Stop early if perfect solution is found
        if best_fitness == 0:
            break

    return best_solution, best_fitness




# Task ID : [est time(hrs),difficulty,deadline(hrs from now),required skill]
task_data = {
    0 : [4, 3, 8, "A"],
    1 : [6, 5, 12, "B"],
    2 : [2, 2, 6, "A"],
    3 : [5, 4, 10, "C"],
    4 : [3, 1, 7, "A"],
    5 : [8, 6, 15, "B"],
    6 : [4, 3, 9, "C"],
    7 : [7, 5, 14, "B"],
    8 : [2, 2, 5, "A"],
    9 : [6, 4, 11, "C"]
}

# Employee (Emp) ID : [available hours,skill level,skills]
emp_data = {
    0 : [10, 4, ["A", "C"]],
    1 : [12, 6, ["A", "B", "C"]],
    2 : [8, 3, ["A"]],
    3 : [15, 7, ["B", "C"]],
    4 : [9, 5, ["A", "C"]]
}

# Run the ACO algorithm
best_solution, best_fitness = ant_colony_optimization(30, 0.3, 1, 500, task_data, emp_data)
    
    


print("\nBest solution:", best_solution)
print("Best fitness:", best_fitness)
print("\Graph:")
print_board(best_solution)
