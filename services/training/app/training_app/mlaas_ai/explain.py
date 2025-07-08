import joblib
import shap
from .config import Config

cfg = Config()

def explain_instance(model, X_instance):
    explainer = shap.Explainer(model, X_instance)
    shap_values = explainer(X_instance).values.tolist()
    return shap_values

def load_model(artifact_path):
    return joblib.load(artifact_path)
