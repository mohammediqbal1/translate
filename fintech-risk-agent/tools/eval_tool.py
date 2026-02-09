from sklearn.metrics import precision_score, recall_score, accuracy_score

def evaluate_model(y_test, preds):
    precision = precision_score(y_test, preds, zero_division=0)
    recall = recall_score(y_test, preds, zero_division=0)
    accuracy = accuracy_score(y_test, preds)

    return {
        "precision": precision,
        "recall": recall,
        "accuracy": accuracy
    }
