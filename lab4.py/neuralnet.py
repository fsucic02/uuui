import numpy as np

class NeuralNetwork:
    def __init__(self, input_dim, hidden_layers, output_dim, init_weights=True):
        self.input_dim = input_dim
        self.hidden_layers = hidden_layers
        self.output_dim = output_dim
        self.layers = [] #  for every layer we need to know the weights, bias vector and activation function

        if init_weights:
            prev_input_dim = input_dim
            for out_layer in hidden_layers:
                w = np.random.normal(scale=0.01, size=(out_layer, prev_input_dim))
                b = np.random.normal(scale=0.01, size=(1, out_layer))
                self.layers.append((w, b, lambda x: 1 / (1 + np.exp(-x)))) # sigmoid
                prev_input_dim = out_layer

            out_layer_w = np.random.normal(scale=0.01, size=(output_dim, prev_input_dim))
            out_layer_b = np.random.normal(scale=0.01, size=(1, output_dim))
            self.layers.append((out_layer_w, out_layer_b, lambda x: x)) # identity for last layer

    def forward(self, X):
        output = X
        for w, b, function in self.layers:
            output = function(np.dot(output, w.T) + b)
        return output

    def mse(self, Y_true, Y_pred):
        return np.mean((np.expand_dims(Y_true, axis=1) - Y_pred) ** 2)
    