import classes

def get_data(task_filename, employee_filename):
    tasks = []
    employees = []

    with open(task_filename, 'r') as task_file:
        try:
            _ = task_file.readline() # Consume header line
            for line in task_file:
                line = line.strip('\n')
                ID, estTime, difficulty, deadline, requiredSkill = line.split(",")
                task = classes.task(ID, int(estTime), int(difficulty), int(deadline), requiredSkill)
                tasks.append(task)  # add task to the list
        except ValueError:
            print("Bad task file. Integer expected")
            return None

    with open(employee_filename, 'r') as employee_file:
        try:
            _ = employee_file.readline() # Consume header line
            for line in employee_file:
                line = line.strip('\n')
                ID, availableHours, skillLevel, skills = line.split(",")
                employee = classes.employee(ID, int(availableHours), int(skillLevel), list(skills))  # setting remainingHours to availableHours
                employees.append(employee)  # add employee to the list
        except ValueError:
            print("Bad employee file. Integer expected")
            return None

    return (tasks, employees)
