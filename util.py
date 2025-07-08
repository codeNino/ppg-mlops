import os


from enum import Enum

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

def validate_gender(value: str) -> Gender:
    try:
        return Gender(value.capitalize())
    except ValueError:
        raise ValueError(f"Invalid gender: {value}. Must be 'Male' or 'Female'.")


def list_csv_files(folder_path):
    """
    Returns a list of all CSV files in the specified folder.

    Parameters:
    - folder_path (str): Path to the folder to search for CSV files.

    Returns:
    - List[str]: List of full paths to CSV files.
    """
    return [os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if file.endswith('.csv')]


def extract_id_from_path(file_path):
    """
    Extracts the substring after 'signal_' or 'label_' from the given file path.

    Parameters:
    - file_path (str): The full file path.

    Returns:
    - str: The substring after 'signal_' or 'label_', or None if neither is found.
    """
    import re
    match = re.search(r'(signal_|label_)(.+?)\.csv', file_path)
    return match.group(2) if match else None
