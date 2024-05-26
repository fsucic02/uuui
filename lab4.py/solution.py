import argparse
from utils import load_data
from genalg import genetic_algorithm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    arguments = ['--train', '--test', '--nn', '--popsize', '--elitism', '--p', '--K', '--iter']
    for argument in arguments:
        parser.add_argument(argument)
    args = parser.parse_args()
    
    train_path, test_path, nn_architecture, popsize, elitism, p, K, iter_num = args.train, args.test, args.nn, int(args.popsize), int(args.elitism), float(args.p), float(args.K), int(args.iter)
    X_train, Y_train, input_dim = load_data(train_path)
    best_network = genetic_algorithm(input_dim, nn_architecture, 1, popsize, elitism, p, K, iter_num, X_train, Y_train)

    X_test, Y_test, _ = load_data(test_path)
    predictions = best_network.forward(X_test)
    print(f"[Test error]: {best_network.mse(Y_test, predictions):.6f}")