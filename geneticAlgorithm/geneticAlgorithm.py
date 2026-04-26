import random
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import candidateGeneration as cG

random.seed(2009)

def geneticAlgorithm(tasks, employees, N):
    candidates = cG.generateCandidates(tasks, employees, N, flawed=True)

    #! sort then figure out a way to unsort


    #print(candidates)

    totalFitness = computeTotalFitness(candidates)
    
    
    generation = 0
    terminationCondition = False
    maxGenerations = 200 #100
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

            newPopulation.append(offspring1)
            newPopulation.append(offspring2)

        candidates = newPopulation
        generation += 1
        meanFitness = computeTotalFitness(candidates) / len(candidates) if candidates else 0
        print(f"Generation {generation}: Mean Fitness: {round(meanFitness, 2)}")

    bestCandidate = GetBestIndividual(candidates)
    return bestCandidate


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
            # Swap the assigned employees between two tasks, keeping task order
            swapIndex = random.randint(0, len(candidate) - 1)
            if i != swapIndex:
                # Each element: (task, employee, time_spent)
                t1, e1, ts1 = candidate[i]
                t2, e2, ts2 = candidate[swapIndex]
                # Swap employees, keep tasks and time_spent
                candidate[i] = (t1, e2, ts1)
                candidate[swapIndex] = (t2, e1, ts2)
    #print("Mutated Candidate:", candidate)
    return candidate

def EvaluateFitness(candidate):
    fitness = (5 - cG.calculateTotalPenalty(candidate))  # Negate penalty to convert to fitness
    return fitness

def computeTotalFitness(candidates):
    totalFitness = 0
    for candidate in candidates:
        #! what is the actual base fitness value
        totalFitness += EvaluateFitness(candidate)
    return totalFitness

def selectParent(candidates, totalFitness):
    pick = random.uniform(0, totalFitness)
    current = 0
    for candidate in candidates:
        current += EvaluateFitness(candidate)
        if current > pick:
            return candidate
    if candidates:
        #! this fails when operating with lower N values for unknown reasons
        print("Warning: No candidate selected during parent selection. Returning a random candidate.")
        return random.choice(candidates)
    return None

def GetBestIndividual(candidates):
    bestCandidate = None
    bestFitness = float('-inf')
    for candidate in candidates:
        fitness = EvaluateFitness(candidate)
        if fitness > bestFitness:
            bestFitness = fitness
            bestCandidate = candidate
    print(f"Best Candidate: {bestCandidate} with Fitness: {bestFitness}")
    return bestCandidate