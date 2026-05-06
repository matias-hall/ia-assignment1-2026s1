import numpy as np
import matplotlib.pyplot as plt
from data import get_data
import particleSwarmOptimisation.particleSwarmOptimisation as pSO

# Graph tuning parameters
res = 10
w_range = [0.6, 1.0]
c_range = [0.5, 3.0]
swarm_range = [10, 40]
trials = 10

def tune_wc(tasks, employees):
    results = np.zeros(shape=(res,res), dtype=np.float64)
    for i, w in enumerate(np.linspace(*w_range, res)):
        for j, c in enumerate(np.linspace(*c_range, res)):
            for trial in range(trials):
                result, score = pSO.particle_swarm_optimisation(tasks, employees, w=w, c1=c, c2=c, max_iterations=250)
                results[i, j] = results[i, j] + score
            results[i, j] = results[i, j] / trials

    w = np.linspace(*w_range, res)
    c = np.linspace(*c_range, res)
    X, Y = np.meshgrid(w, c)
    print(X)
    print(Y)
    Z = results
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

def tune_cs(tasks, employees):
    results = np.zeros(shape=(res,res), dtype=np.float64)
    for i, c1 in enumerate(np.linspace(*c_range, res)):
        for j, c2 in enumerate(np.linspace(*c_range, res)):
            for trial in range(trials):
                result, score = pSO.particle_swarm_optimisation(tasks, employees, w=0.82, c1=c1, c2=c2, max_iterations=250)
                results[i, j] = results[i, j] + score
            results[i, j] = results[i, j] / trials

    c1 = np.linspace(*c_range, res)
    c2 = np.linspace(*c_range, res)
    X, Y = np.meshgrid(c1, c2)
    print(X)
    print(Y)
    Z = results
    print(Z)
    fig, ax = plt.subplots()
    CS = ax.contourf(X, Y, Z, cmap='viridis_r')
    cbar = fig.colorbar(CS)
    cbar.ax.set_ylabel('Result (low is better)')
    ax.set_title(f'Hyperparameter plot (resolution: {res}, trials: {trials})')
    ax.set_xlabel('c1')
    ax.set_ylabel('c2')
    ax.set_xbound(*c_range)
    ax.set_ybound(*c_range)
    plt.savefig('tuning.png')

def tune_swarm_size(tasks, employees):
    start = swarm_range[0]
    end = swarm_range[1] + 1
    tests = range(start, end, res)

    fig, ax = plt.subplots()
    ax.set_title(f'Swarm size (trials: {trials})')

    X = np.zeros(shape=(trials,len(tests)))

    for i, swarm_size in enumerate(tests):
        for j, trial in enumerate(range(trials)):
            result, score = pSO.particle_swarm_optimisation(tasks, employees, swarm_size=swarm_size)
            X[j, i] = score

    ax.hist(X, bins=4, rwidth=0.5, label=tests)
    ax.set_xlabel('Penalty (lower is better)')
    ax.set_ylabel('Frequency')
    ax.legend()
    plt.savefig('swarm_tuning.png')

def simple_statistics(tasks, employees):
    data = np.empty(shape=(200))
    for i in range(200):
        result, score = pSO.particle_swarm_optimisation(tasks, employees, max_iterations=500)
        data[i] = score
    minimum = np.min(data)
    maximum = np.max(data)
    average = np.average(data)
    below_two = np.count_nonzero(data <= 0.21)
    print(f'Range: [{minimum}, {maximum}]\nAverage: {average}\n{below_two}/200 ({below_two/200}) below 0.2')

# Produce various tunining graphs.
# Uncomment to run.
# tune_wc(*get_data('taskdata.csv', 'employeedata.csv'))
# tune_cs(*get_data('taskdata.csv', 'employeedata.csv'))
# tune_swarm_size(*get_data('taskdata.csv', 'employeedata.csv'))
# simple_statistics(*get_data('taskdata.csv', 'employeedata.csv'))
