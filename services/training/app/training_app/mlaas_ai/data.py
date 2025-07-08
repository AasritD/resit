import pandas as pd
import numpy as np
import joblib
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from .config import Config

cfg = Config()

def ingest() -> None:
    raw = pd.read_csv(cfg.raw_csv)
    y = raw['target'].values
    X = raw.drop(columns=['target'])
    
    num_cols = X.select_dtypes(include=['int64','float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object','category']).columns.tolist()
    
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', RobustScaler())
    ])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])
    
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ], sparse_threshold=0)
    
    X_proc = preprocessor.fit_transform(X)
    
    # Save artifacts
    joblib.dump(preprocessor, cfg.preprocessor_path)
    np.savez_compressed(cfg.cleaned_npz, X=X_proc, y=y)
    print(f"Ingested: {cfg.raw_csv} → {cfg.cleaned_npz}, {cfg.preprocessor_path}")
