from utils import load_data, Node, most_common_label, subset, print_information_gains, get_possible_feature_values
from math import log2

class ID3():
    def __init__(self, max_depth):
        self.tree = None
        self.train_dataset = None
        self.max_depth = max_depth

    def fit(self, train_dataset):
        self.train_dataset = train_dataset
        D, D_parent, X = load_data(train_dataset)
        self.tree = self.id3(D, D_parent, X, 0)
        #print(self.tree)
        self.print_tree()

    def predict(self, test_dataset):
        return [self._predict(example, self.tree) for example in test_dataset]

    def _predict(self, example, node, valid_features=None):
        if not valid_features:
            valid_features = []

        if not node.subtrees: # Leaf
            return node.value

        feature_value = example.get(node.value, [])
        if feature_value in node.subtrees:
            return self._predict(example, node.subtrees[feature_value], valid_features + [node.value])
        else:
            if len(valid_features) == 0:
                return most_common_label(self.train_dataset)
            else:
                return most_common_label([e for e in self.train_dataset
                                        if all(example[feature] == e[feature] for feature in valid_features)])
                
    
    def id3(self, D, D_parent, X, depth):
        if self.max_depth is not None and depth >= self.max_depth:
            return Node(most_common_label(D), None)
        
        if len(D) == 0:
            v = most_common_label(D_parent)
            return Node(v, None)

        v = most_common_label(D)
        if X is None or D == subset(D, v):
            return Node(v, None)
        
        x = self.most_discriminative_feature(D, X)[0] # index 0 because this returns tuple (feature, information_gain)
        X_new = X.copy()
        X_new.remove(x)
        subtrees = {}
        for value in get_possible_feature_values(D, x):
            t = self.id3([example for example in D if example[x] == value], D, X_new, depth+1)
            subtrees[value] = t
        return Node(x, subtrees)

    def calculate_entropy(self, D):
        entropy = 0
        y = list(D[0].keys())[-1]
        denom = len(D)
        possible_y_values = get_possible_feature_values(D, y)
        for value in possible_y_values:
            x = len([example for example in D if example[y] == value]) / denom
            entropy += x * log2(x)
        return -entropy

    def calculate_information_gain(self, D, feature):
        possible_feature_values = get_possible_feature_values(D, feature)
        feature_info = 0
        for value in possible_feature_values:
            value_data = [example for example in D if example[feature] == value]
            value_entropy = self.calculate_entropy(value_data)
            feature_info += value_entropy * len(value_data) / len(D)
        return round(self.calculate_entropy(D) - feature_info, 4)

    def most_discriminative_feature(self, D, X):
        gains = {}
        for feature in X:
            information_gain = self.calculate_information_gain(D, feature)
            gains[feature] = information_gain
        gains = dict(sorted(gains.items(), key=lambda x: (-x[1], x[0])))
        print_information_gains(gains)
        return list(gains.items())[0]

    def print_tree(self):
        print('[BRANCHES]:')
        self.print_tree_recursive(self.tree, 1)

    def print_tree_recursive(self, node, depth, path=None):
        if path is None:
            path = []

        if not node.subtrees:
            path.append((depth, node.value))
            self.print_path(path)
        else:
            for key, subtree in node.subtrees.items():
                self.print_tree_recursive(subtree, depth+1, path + [(depth, f"{node.value}={key}")])

    def print_path(self, path):
        print(' '.join(f"{depth}:{value}" if '=' in value else f"{value}"
        for depth, value in path))
