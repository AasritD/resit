from dataclasses import dataclass, field
import os

@dataclass
class Config:
    raw_csv: str = os.getenv('RAW_CSV', 'data/Synthetic_Data_For_Students.csv')
    cleaned_npz: str = os.getenv('CLEANED_NPZ', 'data/cleaned_data.npz')
    preprocessor_path: str = os.getenv('PREPROCESSOR_PATH', 'models/preprocessor.joblib')
    mlflow_uri: str = os.getenv('MLFLOW_TRACKING_URI', 'http://mlflow:5000')
    mlflow_experiment: str = 'mlaas_experiment'
    random_state: int = 42
    test_size: float = 0.2
    optuna_trials: int = 50
    protected_attrs: list = field(default_factory=lambda: ['gender', 'age'])
