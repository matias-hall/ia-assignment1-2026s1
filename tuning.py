import numpy as np
import matplotlib.pyplot as plt
from data import get_data
import particleSwarmOptimisation.particleSwarmOptimisation as pSO

res = 15
w_range = [0.6, 1.4]
c_range = [1.5, 3]
trials = 8

def tune_pso(tasks, employees):
    results = np.empty(shape=(res,res), dtype=np.float)
    for i, w in enumerate(np.linspace(*w_range, res)):
        for j, c in enumerate(np.linspace(*c_range, res)):
            results[i, j] = 0
            for trial in range(trials):
                result, score = pSO.particle_swarm_optimisation(tasks, employees, w=w, c1=c, c2=c)
                results[i, j] = results[i, j] + score
            results[i, j] = results[i, j] / trials
    return results

def graph_tuning(tuning):
    w = np.linspace(*w_range, res)
    c = np.linspace(*c_range, res)
    X, Y = np.meshgrid(w, c)
    print(X)
    print(Y)
    Z = tuning
    print(Z)
    fig, ax = plt.subplots()
    CS = ax.contourf(X, Y, Z, cmap='viridis_r')
    cbar = fig.colorbar(CS)
    cbar.ax.set_ylabel('Result (low is better)')
    ax.plot(c - 1, c, linestyle='-', color='k', linewidth=1)
    ax.set_title(f'Hyperparameter plot (resolution: {res}, trials: {trials})')
    ax.set_xlabel('w')
    ax.set_ylabel('c')
    ax.set_xbound(*w_range)
    ax.set_ybound(*c_range)
    plt.savefig('tuning.png')

results = tune_pso(*get_data('taskdata.csv', 'employeedata.csv'))
graph_tuning(results)
