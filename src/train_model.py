import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


def train_model(csv_path: str, model_path: str = "model.pkl") -> None:
    df = pd.read_csv(csv_path)
    y = df.pop("price")
    X = pd.get_dummies(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    print(f"MAE: {mae:.2f}")

    import joblib
    joblib.dump(model, model_path)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Train price prediction model")
    parser.add_argument("--csv", default="work/etl_used_mansion.csv", help="Training data")
    parser.add_argument("--model", default="work/model.pkl", help="Model output path")
    args = parser.parse_args()

    train_model(args.csv, args.model)
