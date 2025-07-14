import os
import pandas as pd
from src.utils.read_files import read_yaml

if __name__ == '__main__':

    # run as module: python -m src.utils.read_files

    FILE = os.path.join('src', 'utils', 'data_model.yml')

    loaded_file = read_yaml(file_path=FILE)

    columns = loaded_file['transaction-db']

    print(columns)



