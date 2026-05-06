import random
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import tracemalloc
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import candidateGeneration as cG

random.seed(2009)

def geneticAlgorithm(tasks, employees, N, maxGenerations, crossoverRate, mutationRate, return_mean_fitness=False):
    candidates = cG.generateCandidates(tasks, employees, N, flawed=True)
    totalFitness = computeTotalFitness(candidates)
    generation = 0
    terminationCondition = False
    meanFitness = 0
    while generation <= maxGenerations and not terminationCondition:
        newPopulation = []
        while len(newPopulation) < len(candidates):
            parent1 = selectParent(candidates, totalFitness)
            parent2 = selectParent(candidates, totalFitness)
            if (random.random() < crossoverRate):
                offspring1, offspring2 = crossover(parent1, parent2)
            else:
                offspring1, offspring2 = parent1, parent2
            offspring1 = mutate(offspring1, mutationRate)
            offspring2 = mutate(offspring2, mutationRate)
            newPopulation.append(offspring1)
            newPopulation.append(offspring2)
        candidates = newPopulation
        meanFitness = computeTotalFitness(candidates) / len(candidates) if candidates else 0
        generation += 1
    bestCandidate = GetBestIndividual(candidates)
    if return_mean_fitness:
        return bestCandidate, meanFitness
    return bestCandidate

def crossover(parent1, parent2):
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
            # swapping candidates
            swapIndex = random.randint(0, len(candidate) - 1)
            if i != swapIndex:
                t1, e1, ts1 = candidate[i]
                t2, e2, ts2 = candidate[swapIndex]
                candidate[i] = (t1, e2, ts1)
                candidate[swapIndex] = (t2, e1, ts2)
    return candidate

def EvaluateFitness(candidate):
    fitness = (5 - cG.calculateTotalPenalty(candidate))  # Negate penalty to convert to fitness
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

def evaluateGAConstraints(tasks, employees, N):
    minCR = 0.5
    maxCR = 0.9
    CRinterval = (maxCR - minCR) / 10
    minMR = 0.005
    maxMR = 0.1
    MRinterval = (maxMR - minMR) / 10

    CR_values = [minCR + i * CRinterval for i in range(11)]
    MR_values = [minMR + i * MRinterval for i in range(11)]
    best_fitness_matrix = np.zeros((len(CR_values), len(MR_values)))
    mean_fitness_matrix = np.zeros((len(CR_values), len(MR_values)))
    num_trials = 5

    for i, CR in enumerate(CR_values):
        for j, MR in enumerate(MR_values):
            best_fitnesses = []
            mean_fitnesses = []
            print(f"Evaluating GA with Crossover Rate: {CR:.3f} and Mutation Rate: {MR:.3f}")
            for trial in range(num_trials):
                bestCandidate, finalMeanFitness = geneticAlgorithm(tasks, employees, N, maxGenerations=100, crossoverRate=CR, mutationRate=MR, return_mean_fitness=True)
                fitness = EvaluateFitness(bestCandidate)
                best_fitnesses.append(fitness)
                mean_fitnesses.append(finalMeanFitness)
                print(f"  Trial {trial+1}: Best Fitness: {fitness}, Mean Fitness: {finalMeanFitness}")
            avg_best_fitness = np.mean(best_fitnesses)
            avg_mean_fitness = np.mean(mean_fitnesses)
            best_fitness_matrix[i, j] = avg_best_fitness
            mean_fitness_matrix[i, j] = avg_mean_fitness
            print(f"Averages for CR={CR:.3f}, MR={MR:.3f}: Best Fitness={avg_best_fitness}, Mean Fitness={avg_mean_fitness}\n")

    # heatmaps
    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    im1 = axs[0].imshow(best_fitness_matrix, aspect='auto', origin='lower',
                        extent=[minMR, maxMR, minCR, maxCR], cmap='viridis')
    axs[0].set_title('Best Candidate Fitness')
    axs[0].set_xlabel('Mutation Rate')
    axs[0].set_ylabel('Crossover Rate')
    fig.colorbar(im1, ax=axs[0])

    im2 = axs[1].imshow(mean_fitness_matrix, aspect='auto', origin='lower',
                        extent=[minMR, maxMR, minCR, maxCR], cmap='plasma')
    axs[1].set_title('Final Mean Fitness')
    axs[1].set_xlabel('Mutation Rate')
    axs[1].set_ylabel('Crossover Rate')
    fig.colorbar(im2, ax=axs[1])

    plt.tight_layout()
    plt.show()
    return

def evaluateGAGeneration(tasks, employees, N):
    MG = 500
    num_trials = 5
    best_fitness_matrix = np.zeros((num_trials, MG))
    mean_fitness_matrix = np.zeros((num_trials, MG))

    for trial in range(num_trials):
        print(f"Starting Trial {trial+1}")
        for G in range(1, MG+1):
            bestCandidate, meanFitness = geneticAlgorithm(tasks, employees, N, maxGenerations=G, crossoverRate=0.7, mutationRate=0.01, return_mean_fitness=True)
            fitness = EvaluateFitness(bestCandidate)
            best_fitness_matrix[trial, G-1] = fitness
            mean_fitness_matrix[trial, G-1] = meanFitness


    avg_best_fitness = np.mean(best_fitness_matrix, axis=0)
    avg_mean_fitness = np.mean(mean_fitness_matrix, axis=0)

    generations = np.arange(1, MG+1)
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    for trial in range(num_trials):
        plt.plot(generations, best_fitness_matrix[trial], alpha=0.3, label=f'Trial {trial+1}' if trial==0 else None)
    plt.plot(generations, avg_best_fitness, color='black', linewidth=2, label='Average')
    plt.title('Best Candidate Fitness vs Generations')
    plt.xlabel('Generations')
    plt.ylabel('Constraint Violations')
    plt.legend()

    plt.subplot(1, 2, 2)
    for trial in range(num_trials):
        plt.plot(generations, mean_fitness_matrix[trial], alpha=0.3, label=f'Trial {trial+1}' if trial==0 else None)
    plt.plot(generations, avg_mean_fitness, color='black', linewidth=2, label='Average')
    plt.title('Mean Candidate Fitness vs Generations')
    plt.xlabel('Generations')
    plt.ylabel('Constraint Violations')
    plt.legend()

    plt.tight_layout()
    plt.show()

    # converting from fitness score to constraint violations
    best_fitness_matrix = (best_fitness_matrix - 5) * -num_trials
    mean_fitness_matrix = (mean_fitness_matrix - 5) * -num_trials

    avg_best_fitness = np.mean(best_fitness_matrix, axis=0)
    avg_mean_fitness = np.mean(mean_fitness_matrix, axis=0)

    # plotting
    generations = np.arange(1, MG+1)
    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    for trial in range(num_trials):
        plt.plot(generations, best_fitness_matrix[trial], alpha=0.3, label=f'Trial {trial+1}' if trial==0 else None)
    plt.plot(generations, avg_best_fitness, color='black', linewidth=2, label='Average')
    plt.title('Lowest Constraint Violations vs Generations')
    plt.xlabel('Generations')
    plt.ylabel('Constraint Violations')
    plt.legend()

    plt.subplot(1, 2, 2)
    for trial in range(num_trials):
        plt.plot(generations, mean_fitness_matrix[trial], alpha=0.3, label=f'Trial {trial+1}' if trial==0 else None)
    plt.plot(generations, avg_mean_fitness, color='black', linewidth=2, label='Average')
    plt.title('Mean Constraint Violations vs Generations')
    plt.xlabel('Generations')
    plt.ylabel('Constraint Violations')
    plt.legend()

    plt.tight_layout()
    plt.show()
    return

def evaluateGARuntime(tasks, employees, N):
    MG = 100
    num_trials = 20
    runtime_matrix = np.zeros((num_trials, MG))
    halted_generations = np.full(num_trials, MG)

    for trial in range(num_trials):
        print(f"Starting Trial {trial+1}")
        for G in range(1, MG+1):
            start_time = time.perf_counter()
            bestCandidate, meanFitness = geneticAlgorithm(tasks, employees, N, maxGenerations=G, crossoverRate=0.7, mutationRate=0.01, return_mean_fitness=True)
            end_time = time.perf_counter()
            runtime_matrix[trial, G-1] = end_time - start_time
            # halting implementation
            fitness = EvaluateFitness(bestCandidate)
            if fitness == 5:
                print(f"Halting trial {trial+1} at generation {G} (fitness=5)")
                halted_generations[trial] = G
                break

    # remove values after halting
    masked_runtime_matrix = np.full_like(runtime_matrix, np.nan)
    for trial in range(num_trials):
        halt_gen = halted_generations[trial]
        masked_runtime_matrix[trial, :halt_gen] = runtime_matrix[trial, :halt_gen]
    avg_runtime_per_generation = np.nanmean(masked_runtime_matrix, axis=0)
    generations = np.arange(1, MG+1)
    plt.figure(figsize=(10, 6))
    for trial in range(num_trials):
        plt.plot(generations, runtime_matrix[trial], alpha=0.3, label=f'Trial {trial+1}' if trial==0 else None)
        halt_gen = halted_generations[trial]
        if halt_gen < MG:
            plt.axvline(x=halt_gen, color='red', linestyle='--', alpha=0.5)
    plt.plot(generations, avg_runtime_per_generation, color='black', linewidth=2, label='Average')
    plt.xlabel('Generations')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime per Generation (Halts if fitness=5)')
    plt.legend()
    plt.tight_layout()
    plt.show()
    avg_runtime = np.nanmean([runtime_matrix[trial, halted_generations[trial]-1] for trial in range(num_trials)])
    print(f"Average runtime for halting generation over {num_trials} trials: {avg_runtime:.4f} seconds")