import os
import numpy as np
from mlaas_ai.data import ingest, cfg
def test_ingest(tmp_path, monkeypatch):
    # prepare small CSV
    df = pd.DataFrame({'num':[1, np.nan], 'cat':['a','b'], 'target':[10,20]})
    csv = tmp_path/"d.csv"; df.to_csv(csv,index=False)
    monkeypatch.setenv('RAW_CSV', str(csv))
    monkeypatch.setenv('CLEANED_NPZ', str(tmp_path/"clean.npz"))
    monkeypatch.setenv('PREPROCESSOR_PATH', str(tmp_path/"prep.joblib"))
    ingest()
    assert os.path.exists(tmp_path/"clean.npz")
    assert os.path.exists(tmp_path/"prep.joblib")
