import sys
from decisiontree import ID3
from utils import print_predictions, extract_datasets, print_accuracy, print_confusion_matrix

if __name__ == '__main__':
    train_dataset, test_dataset, max_depth = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) == 4 else None
    train_dataset, test_dataset = extract_datasets(train_dataset, test_dataset)
    model = ID3(max_depth) 
    model.fit(train_dataset)
    predictions = model.predict(test_dataset)
    print_predictions(predictions)
    print_accuracy(test_dataset, predictions)
    print_confusion_matrix(test_dataset, predictions)