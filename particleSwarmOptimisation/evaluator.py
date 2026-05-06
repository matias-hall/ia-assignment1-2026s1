from classes import task, employee

# Class for evaluating a given assignment.
# First, it is loaded with a list of tasks and employees
# Then, the `evaluate_assignment` method can be called with a list of assignments, which results a floating-point number representing the cost.
# The list of assignments should be a list of T integers in the range [1,5], where T is the number of tasks. Each integer represents an employee (there are five employees)
class Evaluator():
    def __init__(self, tasks: list[task], employees: list[employee]):
        self.tasks = tasks
        self.employees = employees

    def evaluate_assignment(self, assignment: list[int]) -> float:
        overload = 0
        for employee_index in range(len(self.employees)):
            # + 1 since employee ids are 1-indexed
            assigned_tasks = [i for i, x in enumerate(assignment) if x == employee_index + 1]
            total_time = 0
            for task_index in assigned_tasks:
                total_time += self.tasks[task_index].estTime

            overload += max(0, total_time - self.employees[employee_index].availableHours)

        skill_mismatch = 0
        for task_index, employee_id in enumerate(assignment):
            required_skill = self.tasks[task_index].requiredSkill
            # - 1 since employee ids are 1-indexed
            skillset = self.employees[employee_id - 1].skills

            if required_skill not in skillset:
                skill_mismatch += 1

        difficulty_violation = 0
        for task_index, employee_id in enumerate(assignment):
            difficulty = self.tasks[task_index].difficulty
            skill_level = self.employees[employee_id - 1].skillLevel

            difficulty_violation += max(0, difficulty - skill_level)

        deadline_violation = 0
        for employee_index in range(len(self.employees)):
            # + 1 since employee ids are 1-indexed
            assigned_tasks = [self.tasks[i] for i, x in enumerate(assignment) if x == employee_index + 1]

            assigned_tasks.sort(key=lambda x: x.estTime)
            time_taken = 0
            for task in assigned_tasks:
                time_taken += task.estTime
                deadline_violation += max(0, time_taken - task.deadline)

        return 0.2 * (overload + skill_mismatch + difficulty_violation + deadline_violation)
