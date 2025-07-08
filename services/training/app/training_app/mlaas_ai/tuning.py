import optuna
from sklearn.model_selection import train_test_split
from .model import train_advanced, load_data
from sklearn.metrics import mean_absolute_percentage_error
from .tracking import start_mlflow_run
from .config import Config

cfg = Config()

def objective(trial):
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=cfg.test_size, random_state=cfg.random_state
    )
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),
        "max_depth": trial.suggest_int("max_depth", 3, 12),
        "learning_rate": trial.suggest_loguniform("learning_rate", 1e-3, 1e-1),
    }
    with start_mlflow_run("optuna_tuning") as run:
        model = GradientBoostingRegressor(**params, random_state=cfg.random_state)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        mape = mean_absolute_percentage_error(y_test, preds) * 100
        # Log params & metric
        run.log_params(params)
        run.log_metric("mape", mape)
    return mape

def run_tuning():
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=cfg.optuna_trials)
    print("Best trial:", study.best_trial.params, "MAPE:", study.best_value)
