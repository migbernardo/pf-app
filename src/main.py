import os
from fastapi import FastAPI
from pydantic import BaseModel, create_model
from src.utils.data_base import DataBase
from src.utils.file_io import np_python_dtype_converter

data_dir = os.path.join('src', 'data')

# set mode as execution parameter
db = DataBase(mode='read', data_path=data_dir, write_schema=False)

# create request models
transaction_req_schema = {col: (dtype, None) for col, dtype in np_python_dtype_converter(data_types=db.schema).items()}

transaction_req_model =  create_model('Transaction', **transaction_req_schema)

# uvicorn src.main:app
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/add_transaction/")
def add_transaction():
    return None