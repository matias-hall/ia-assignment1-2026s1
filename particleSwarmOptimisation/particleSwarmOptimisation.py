import random
import itertools
import numpy as np
from .evaluator import Evaluator

class Particle():
    def __init__(self, position: list[int], velocity: list[float], evaluator: Callable[[Assignment], float]):
        self.position = np.array(position, dtype='i8')
        self.velocity = np.array(velocity, dtype='f8')
        self.evaluator = evaluator
        self.best = position
        self.best_score = evaluator(position)

    # Update its position and reevaluate its personal best
    def tick(self):
        self.position = np.clip((self.position + self.velocity).astype(np.int32), 1, 5)
        print(self.position)

        new_score = self.evaluator(self.position)
        if self.best_score > new_score:
            self.best_score = new_score
            self.best = self.position

    # Update its velocity based on parameters, global best, and its own personal best
    def update_velocity(self, w: float, c1: float, c2: float, global_best):
        self.velocity = (w * self.velocity
                         + random.uniform(0, c1) * (self.best - self.position)
                         + random.uniform(0, c2) * (global_best - self.position))


def _pso_algorithm(population: list[Particle], termination_condition: Callable[[list[Particle]], bool], **params) -> Assignment:
    # Set parameters, with defaults if not given
    w = params.get('w', 0.5)
    c1 = params.get('c1', 1.5)
    c2 = params.get('c2', 1.5)

    global_best = min(population, key=lambda x: x.best_score).best

    while not termination_condition(population):
        # Update the velocity, position, and personal best of each particle
        for individual in population:
            individual.update_velocity(w, c1, c2, global_best)
            individual.tick()
            print(f"Personal best: {individual.best} ({individual.best_score})")
        # Obtain the new global best
        global_best = min(population, key=lambda x: x.best_score).best

    return global_best

# Returns a function that checks whether the solution has converged
# or whether *threshold* iterations have passed.
def _converge_or_threshold(threshold):
    counter = threshold
    def _converge(population):
        nonlocal counter
        counter -= 1
        if counter <= 0:
            return True

        positions = map(lambda particle: particle.position, population)

        first = next(positions)
        for p in positions:
            # If any spots in the array differ, then it hasn't converged yet
            if np.any(p != first):
                return False
        return True
    return _converge

# Particle swarm optimisation algorithm:
# *tasks* is list of tasks
# *employees* is list of employees
# *swarm_size* is the number of particles to run, default is 15
# *max_iterations* is the maximum number of iterations to run before returning, default is 100
# Additional parameters passed to internal pso algorithm:
# *w* is the inertia, default 0.5
# *c1* is the personal influence learning factor, default 1.5
# *c2* is the social influence learning factor, default 1.5
# Returns the best assignment found and its score.
def particle_swarm_optimisation(tasks: list[task], employees: list[employee], swarm_size: int=15, max_iterations: int=100, **params) -> (list[int], float):
    evaluator = Evaluator(tasks, employees)
    population = []
    for i in range(swarm_size):
        # Randomly choose an employee 1 to 5 to complete each task
        assignment = random.choices(range(1, 6), k=10)
        # velocity is made up of random floats in the range (-2, 2)
        # This might be a parameter worth tuning
        velocity = []
        for i in range(10):
            velocity.append(random.uniform(-2.0, 2.0))
        population.append(Particle(assignment, velocity, evaluator.evaluate_assignment))

    result = _pso_algorithm(population, _converge_or_threshold(max_iterations), **params)
    return result, evaluator.evaluate_assignment(result)
