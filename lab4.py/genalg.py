from utils import construct_network
from neuralnet import NeuralNetwork
import numpy as np

def genetic_algorithm(input_dim, nn_architecture, output_dim, popsize, elitism, p, K, iter_num, X_train, Y_train):
    population = [construct_network(input_dim, nn_architecture, output_dim) for _ in range(popsize)]
    
    for iteration in range(1, iter_num + 1):
        fitnesses = np.array([evaluate_fitness(network, X_train, Y_train) for network in population])
        
        sorted_indices = np.argsort(fitnesses)
        population = [population[index] for index in sorted_indices]
        fitnesses = fitnesses[sorted_indices]
        
        next_generation = [population[index] for index in range(-elitism, 0)]
        
        while len(next_generation) < popsize:
            parent_1 = fitness_proportional_selection(population, fitnesses)
            parent_2 = fitness_proportional_selection(population, fitnesses)
            child = crossover(parent_1, parent_2)
            child = mutate(child, p, K)
            next_generation.append(child)
        
        population = next_generation
        
        if iteration % 2000 == 0:
            print(f"[Train error @{iteration}]: {1 / fitnesses[-1]:.6f}")
    return population[-1]

def crossover(parent_1, parent_2):
    child = NeuralNetwork(parent_1.input_dim, parent_1.hidden_layers, parent_1.output_dim, init_weights=False)
    for i in range(len(parent_1.layers)):
        w, b, function = (parent_1.layers[i][0] + parent_2.layers[i][0]) / 2, (parent_1.layers[i][1] + parent_2.layers[i][1]) / 2, parent_1.layers[i][2]
        child.layers.append((w, b, function))
    return child

def mutate(network, p, K):
    for idx, (w, b, function) in enumerate(network.layers):
        mutation_mask = np.random.rand(*w.shape) < p
        mutations = np.random.normal(scale=K, size=w.shape)
        mutated_w = w + mutation_mask * mutations

        mutation_mask = np.random.rand(*b.shape) < p
        mutations = np.random.normal(scale=K, size=b.shape)
        mutated_b = b + mutation_mask * mutations

        network.layers[idx] = (mutated_w, mutated_b, function)
    return network

def fitness_proportional_selection(population, fitnesses):
    # code taken from: https://stackoverflow.com/questions/10324015/fitness-proportionate-selection-roulette-wheel-selection-in-python
    max = sum(fitnesses)
    selection_probs = fitnesses / max
    return population[np.random.choice(len(population), p=selection_probs)]

def evaluate_fitness(network, X, Y):
    predictions = network.forward(X)
    return 1 / network.mse(Y, predictions)