import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_model(data_path):
    df = pd.read_csv(data_path)

    X = df.drop("default", axis=1)
    y = df["default"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42
    )

    model.fit(X_train, y_train)

    joblib.dump(model, "models/risk_model.pkl")

    return X_test, y_test