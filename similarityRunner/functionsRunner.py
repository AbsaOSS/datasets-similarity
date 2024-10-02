import pandas as pd

from models.connector_models import FileType


def load_files_from_list(folder: list[str], file_types: tuple = (FileType.CSV,)) -> tuple[list[pd.DataFrame], list[str]]:
    """ """
    data = []
    names = []
    for file in folder:
        if FileType.CSV in file_types and file.endswith(".csv"):
            data.append(pd.read_csv(file))
            names.append(file.replace(".csv", ""))
        if FileType.PARQUET in file_types and file.endswith(".parquet"):
            data.append(pd.read_parquet(file))
            names.append(file.replace(".parquet", ""))
    return data, names


def csv_to_parquet(file: str):
    df = pd.read_csv(file)
    df.to_parquet(file.replace(".csv", ".parquet"))
    return file.replace(".csv", ".parquet")
