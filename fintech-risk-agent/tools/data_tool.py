import pandas as pd

def inspect_data(path):
    df = pd.read_csv(path)
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "columns": list(df.columns),
        "target_distribution": df["default"].value_counts().to_dict()
    }
