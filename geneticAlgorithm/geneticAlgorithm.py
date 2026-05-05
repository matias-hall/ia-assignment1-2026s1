import random
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import candidateGeneration as cG

random.seed(2009)

def geneticAlgorithm(tasks, employees, N, maxGenerations, crossoverRate, mutationRate):
    candidates = cG.generateCandidates(tasks, employees, N, flawed=True)

    #! sort then figure out a way to unsort


    #print(candidates)

    totalFitness = computeTotalFitness(candidates)
    
    generation = 0
    terminationCondition = False

    """
    maxGenerations = 500 #100
    crossoverRate = 0.7
    mutationRate = 0.01
    """

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

        #for candidate in newPopulation:
            #candidate = cG.update_time_spent(candidate, employees)

        candidates = newPopulation
        meanFitness = computeTotalFitness(candidates) / len(candidates) if candidates else 0
        #print(f"Generation {generation}: Mean Fitness: {round(meanFitness, 2)}")
        generation += 1

    bestCandidate = GetBestIndividual(candidates)
    return bestCandidate

def crossover(parent1, parent2):
    #crossoverPoint = random.randrange(1, len(parent1) - 1)  # select a random crossover point
    crossoverPoint = random.randrange(0, len(parent1))  # select a random crossover point

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
                t1, e1, ts1 = candidate[i]
                t2, e2, ts2 = candidate[swapIndex]
                candidate[i] = (t1, e2, ts1)
                candidate[swapIndex] = (t2, e1, ts2)
    #print("Mutated Candidate:", candidate)
    return candidate

def EvaluateFitness(candidate):
    fitness = (3 - cG.calculateTotalPenalty(candidate))  # Negate penalty to convert to fitness
    return fitness

def computeTotalFitness(candidates):
    totalFitness = 0
    for candidate in candidates:
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

def evaluateGA(tasks, employees, N):
    minCR = 0.5
    maxCR = 0.9
    CRinterval = (maxCR - minCR) / 20
    minMR = 0.005
    maxMR = 0.1
    MRinterval = (maxMR - minMR) / 20

    for CR in [minCR + i * CRinterval for i in range(21)]:
        for MR in [minMR + i * MRinterval for i in range(21)]:
            print(f"Evaluating GA with Crossover Rate: {CR:.3f} and Mutation Rate: {MR:.3f}")
            bestCandidate = geneticAlgorithm(tasks, employees, N, maxGenerations=100, crossoverRate=CR, mutationRate=MR)
            fitness = EvaluateFitness(bestCandidate)
            print(f"Best Candidate Fitness: {fitness}\n")


    return