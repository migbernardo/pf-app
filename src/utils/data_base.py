import os
import pandas as pd
from src.utils.read_files import read_yaml

class DataBase:
    """
    A base class to create the application database
    Attributes:
        schema: evaluated database schema
        df: supporting data frame
    """
    def __init__(self, data_model:dict):
        self.data_model = data_model
        self.schema = self.read_schema()
        self.df = self.create_df()

    def read_schema(self) -> dict:
        """
        Data model parser
        :return: Schema dictionary with the evaluated data types
        """
        return {column: eval(datetype) for column, datetype in self.data_model.items()}

    def create_df(self) -> pd.DataFrame:
        """
        Create database data frame
        :return: Empty pandas data frame based on the defined schema
        """
        df_columns = pd.DataFrame(columns=list(self.schema.keys()))
        df_schema = df_columns.astype(dtype=self.schema)
        return df_schema


if __name__ == '__main__':

    # run as module: python -m src.utils.read_files

    FILE = os.path.join('src', 'utils', 'data_model.yml')

    loaded_file = read_yaml(file_path=FILE)
    loaded_data_model = loaded_file['transaction-db']
    db = DataBase(data_model=loaded_data_model)

    print(db.df.info())