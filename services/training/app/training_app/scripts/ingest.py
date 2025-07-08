import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import numpy as np

def main():
    # 1. Load raw data
    raw = pd.read_csv('data/Synthetic_Data_For_Students.csv')
    
    # 2. Identify feature types
    num_cols = raw.select_dtypes(include=['int64', 'float64']).columns.drop('target').tolist()
    cat_cols = raw.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 3. Build preprocessing pipelines
    num_pipeline = Pipeline([('imputer', SimpleImputer(strategy='median'))])
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='unknown')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])
    preprocessor = ColumnTransformer([
        ('num', num_pipeline, num_cols),
        ('cat', cat_pipeline, cat_cols)
    ])
    
    # 4. Split features/target
    X = raw.drop(columns=['target'])
    y = raw['target'].values
    
    # 5. Fit & transform
    X_proc = preprocessor.fit_transform(X)
    
    # 6. Persist artifacts
    os.makedirs('models', exist_ok=True)
    joblib.dump(preprocessor, 'models/preprocessor.joblib')
    np.savez_compressed('data/cleaned_data.npz', X=X_proc, y=y)
    
    print('✅ Ingestion complete — cleaned_data.npz and preprocessor.joblib written.')

if __name__ == '__main__':
    main()
