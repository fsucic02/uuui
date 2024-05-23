import csv

class Node:
    def __init__(self, value, subtrees):
        self.value = value
        self.subtrees = subtrees # Leaf will be Node without subtrees

    def __repr__(self):
        return f"Node({self.value}, {self.subtrees})" if self.subtrees is not None else f"Leaf({self.value})"
     
def print_predictions(predictions):
    print('[PREDICTIONS]: ', ' '.join(prediction for prediction in predictions if prediction is not None))

def extract_datasets(train_dataset, test_dataset):
    return [row for row in csv.DictReader(open(train_dataset))], [row for row in csv.DictReader(open(test_dataset))]

def load_data(train_dataset):
    D, D_parent = train_dataset, train_dataset
    X = list(train_dataset[0].keys())[:-1]
    return D, D_parent, X

def most_common_label(D):
    cnt, y = {}, list(D[0].keys())[-1]
    for example in D:
        if cnt.get(example[y], None) is None:
            cnt[example[y]] = 0
        else:
            cnt[example[y]] += 1
    cnt = dict(sorted(cnt.items(), key=lambda x: (-x[1], x[0])))
    return max(cnt, key=cnt.get)

def subset(D, v):
    y = list(D[0].keys())[-1]
    return [example for example in D if example[y] == v]

def get_possible_feature_values(D, feature):
    return set([example[feature] for example in D])

def print_information_gains(gains):
    print(' '.join(f"IG({key})={value:.4f}" for key, value in gains.items()))

def print_accuracy(test_dataset, predictions):
    y = list(test_dataset[0].keys())[-1]
    print(f"[ACCURACY]: {len([prediction for idx, prediction in enumerate(predictions) if prediction == test_dataset[idx][y]]) / len(test_dataset):.5f}")
    
def print_confusion_matrix(test_dataset, predictions):
    print('[CONFUSION_MATRIX]:')
    y = list(test_dataset[0].keys())[-1]
    values = sorted(list(get_possible_feature_values(test_dataset, y)))
    matrix = [[0 for _ in range(len(values))] for _ in range(len(values))]
    for i, pred_value in enumerate(values):
        for j, true_value in enumerate(values):
            matrix[j][i] = len([prediction for idx, prediction in enumerate(predictions) if prediction == pred_value and test_dataset[idx][y] == true_value])
    

    for i in range(len(values)):
        for j in range(len(values)):
            print(matrix[i][j], end=' ')
        print()