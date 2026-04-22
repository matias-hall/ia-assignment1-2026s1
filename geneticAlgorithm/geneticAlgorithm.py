import random
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import candidateGeneration as cG

random.seed(2009)

def geneticAlgorithm(tasks, employees, N):
    candidates = cG.generateCandidates(tasks, employees, N, flawed=True)

    #! sort then figure out a way to unsort

    """

    sortedCandidates = []

    for candidate in sortedCandidates:
            sortedCandidate = sorted(candidate[:-1], key=lambda x: x[0].ID)
            sortedCandidate.append(candidate[-1])  # append the deadline penalty at the end of the sorted candidate

    print(candidates)
    print(sortedCandidates)

    totalFitness = computeTotalFitness(candidates)
    
    generation = 0
    terminationCondition = False
    maxGenerations = 100
    crossoverRate = 0.7
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

def crossover(parent1, parent2):
    crossoverPoint = random.randrange(1, len(parent1) - 1)  # select a random crossover point

    offspring1 = []
    offspring2 = []

    for i in range(crossoverPoint):
        offspring1.append(parent1[i])
        offspring2.append(parent2[i])

    for i in range(crossoverPoint, len(parent1)):
        offspring1.append(parent2[i])
        offspring2.append(parent1[i])

    return offspring1, offspring2

def mutate(candidate, mutationRate):
    for i in range(len(candidate)):
        if random.random() < mutationRate:
            pass  
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

def EvaluateFitness(candidate):
    candidate = cG.calculateDeadlinePenalty(candidate)
    candidate = cG.update_time_spent(candidate, employees)
    return candidate