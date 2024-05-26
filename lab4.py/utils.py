from neuralnet import NeuralNetwork
import numpy as np

def load_data(file_path):
    data = np.loadtxt(file_path, delimiter=',', skiprows=1)
    X = data[:, :-1]
    y = data[:, -1]
    return X, y, len(X[0])

def construct_network(input_dim, nn_architecture, output_dim):
    return NeuralNetwork(input_dim, [int(char) for char in nn_architecture.split('s')[:-1]], output_dim) # sigmoid activation in every layer

