import pandas as pd
from .config import Config
from sklearn.metrics import mean_absolute_percentage_error

cfg = Config()

def compute_group_mape(group, y_true, y_pred):
    return mean_absolute_percentage_error(y_true[group], y_pred[group]) * 100

def fairness_report(model, X, y, raw_df: pd.DataFrame):
    preds = model.predict(X)
    report = {}
    for attr in cfg.protected_attrs:
        for val in raw_df[attr].unique():
            mask = raw_df[attr] == val
            mape = compute_group_mape(mask, y, preds)
            report[f"{attr}={val}"] = mape
    return report
