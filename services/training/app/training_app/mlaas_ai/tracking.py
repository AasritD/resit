import mlflow
from .config import Config
from contextlib import contextmanager

cfg = Config()

@contextmanager
def start_mlflow_run(run_name: str):
    mlflow.set_tracking_uri(cfg.mlflow_uri)
    mlflow.set_experiment(cfg.mlflow_experiment)
    with mlflow.start_run(run_name=run_name) as run:
        yield run
