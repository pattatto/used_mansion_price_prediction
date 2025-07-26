# 中古マンション住宅予測

このリポジトリでは中古マンションの価格予測モデルを扱います。`src/etl.py` で生データの整形を行い、`src/train_model.py` でランダムフォレストによる学習を行います。

## 使い方

1. ETL 処理
    ```bash
    python src/etl.py --excel work/used_mansion.xlsx --output work/etl_used_mansion.csv
    ```
2. モデル学習
    ```bash
    python src/train_model.py --csv work/etl_used_mansion.csv --model work/model.pkl
    ```

依存パッケージは `pandas` と `scikit-learn`、`joblib` です。
