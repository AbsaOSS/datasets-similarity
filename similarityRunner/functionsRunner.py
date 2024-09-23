import pandas as pd

from models.connector_models import FileType


def load_files_from_list(folder: list[str], file_type: tuple[FileType] = FileType.CSV) -> tuple[list[pd.DataFrame], list[str]]:
    """
    it loads cvs files from folder and returns list of loaded dataframe and list of names
    :param folder: from which we load the files
    :param file_type: type of file, csv, parquet, etc.
    :return: two lists
    """
    data = []
    names = []
    for file in folder:
        if FileType.CSV in file_type and file.endswith(".csv"):
            data.append(pd.read_csv(file))
            names.append(file.replace(".csv", ""))
        if FileType.PARQUET in file_type and file.endswith(".parquet"):
            data.append(pd.read_parquet(file))
            names.append(file.replace(".parquet", ""))
    return data, names
