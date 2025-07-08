#!/usr/bin/env python
from sklearn.model_selection import train_test_split
from mlaas_ai.data import ingest
from mlaas_ai.model import train_baseline, train_advanced, load_data
from mlaas_ai.tracking import start_mlflow_run
from mlaas_ai.tuning import run_tuning
from mlaas_ai.fairness import fairness_report
import pandas as pd
import joblib

def main():
    # 1. Ingest & preprocess
    ingest()
    X, y = load_data()
    
    # Optional: load raw df for fairness
    raw = pd.read_csv("data/Synthetic_Data_For_Students.csv")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # 2. Baseline run
    with start_mlflow_run("baseline"):
        model_dt, mape_dt = train_baseline(X_train, y_train, X_test, y_test)
        mlflow.log_metric("dt_mape", mape_dt)
        mlflow.sklearn.log_model(model_dt, "dt_model")
    
    # 3. Advanced run
    with start_mlflow_run("advanced"):
        model_gb, mape_gb = train_advanced(X_train, y_train, X_test, y_test)
        mlflow.log_metric("gb_mape", mape_gb)
        mlflow.sklearn.log_model(model_gb, "gb_model")
        
        # Fairness
        report = fairness_report(model_gb, X_test, y_test, raw.loc[y_test.index])
        mlflow.log_dict(report, "fairness_report.json")
    
    # 4. Hyperparameter tuning
    run_tuning()

if __name__ == "__main__":
    main()
