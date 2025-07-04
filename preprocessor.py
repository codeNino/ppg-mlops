import pandas as pd
from signal_analyzer import extract_ppg_features
from util import extract_id_from_path, list_csv_files

def get_features_from_labels(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df.iloc[0].to_dict()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def get_features_from_ppg(csv_path):
    try:
        df = pd.read_csv(csv_path)
        print("dataframe ")
        ppg_signal = df.iloc[:, 0].values
        print("ppg signal read")
        features = extract_ppg_features(ppg_signal)
        print("features extracted from ppg signal")
        return features
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def get_feature_target_dict(signal_folder: str, label_folder: str):
    extracted_signals, extracted_targets = {} , {}
    signal_file_paths = list_csv_files(signal_folder)
    label_file_paths = list_csv_files(label_folder)
    for path in signal_file_paths:
        id = extract_id_from_path(path)
        features = get_features_from_ppg(path)
        extracted_signals[id] = features
    for path in label_file_paths:
        id = extract_id_from_path(path)
        if id:
            feature_dict = extracted_signals[id]
            labels = get_features_from_labels(path)
            extracted_targets[id] = labels.get("Glucose")
            feature_dict["age"] = labels.get("Age")
            feature_dict["gender"] = labels.get("Gender")
            feature_dict["height"] = labels.get("Height")
            feature_dict["weight"] = labels.get("Weight")
    return extracted_signals, extracted_targets
    




def create_feature_target_df(signal_folder: str, label_folder: str):

    features_dict, targets_dict = get_feature_target_dict(signal_folder, label_folder)
    rows = []

    for user_id, features in features_dict.items():
        if user_id in targets_dict:
            row = features.copy()
            row['glucose'] = targets_dict[user_id]
            rows.append(row)

    return pd.DataFrame(rows)





