import numpy as np
import joblib
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_percentage_error
from .config import Config

cfg = Config()

def load_data():
    arr = np.load(cfg.cleaned_npz)
    return arr['X'], arr['y']

def train_baseline(X_train, y_train, X_test, y_test):
    dt = DecisionTreeRegressor(max_depth=5, random_state=cfg.random_state)
    dt.fit(X_train, y_train)
    preds = dt.predict(X_test)
    mape = mean_absolute_percentage_error(y_test, preds) * 100
    return dt, mape

def train_advanced(X_train, y_train, X_test, y_test):
    gb = GradientBoostingRegressor(random_state=cfg.random_state)
    gb.fit(X_train, y_train)
    preds = gb.predict(X_test)
    mape = mean_absolute_percentage_error(y_test, preds) * 100
    return gb, mape
