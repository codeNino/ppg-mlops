import xgboost as xgb
import pandas as pd
import numpy as np


def get_features_for_prediction(df: pd.DataFrame, features = [
    'mean_ppg', 'std_ppg', 'skew_ppg', 'kurtosis_ppg',
    'mean_hr', 'std_hr', 'lf_power', 'hf_power', 'lf_hf_ratio', 'pulse_rate',
    'age', 'gender'	,'height',	'weight'
]):
    # Ensure the feature columns are present and ordered correctly
    if not all(col in df.columns for col in features):
        missing = [col for col in features if col not in df.columns]
        raise ValueError(f"Missing required columns in CSV: {missing}")

    df_features : pd.DataFrame = df[features]
    cats = df_features.select_dtypes(exclude=np.number).columns.tolist()
    for col in cats:
        df_features[col] = df_features[col].astype('category')

    dmatrix = xgb.DMatrix(df_features, enable_categorical=True)

    return dmatrix

def reload_model(file: str):
    model = xgb.Booster()
    model.load_model(file)
    return model