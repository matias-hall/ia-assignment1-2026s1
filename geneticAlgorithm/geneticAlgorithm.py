#! implement genetic algorithm
import random

random.seed(2009)

#generate N candidate solutions
candidates = []
N = 20

for n in range(N):
    order = [1,2,3,4,5,6,7,8,9,10]
    random.shuffle(order)
    print(order)