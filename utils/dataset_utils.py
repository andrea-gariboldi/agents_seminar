import pandas as pd

def get_columns_from_dataset(dataset_path: str):
    return list(pd.read_csv(dataset_path, nrows=0).columns)

def exclude_column_from_dataset(dataframe: pd.DataFrame, column_name: str):
    return dataframe.drop(columns=[column_name])