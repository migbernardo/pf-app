import os
from fastapi import FastAPI
from pydantic import create_model, BaseModel
from datetime import datetime
from typing import Any
from src.utils.data_base import DataBase
from src.utils.file_io import np_python_dtype_converter

data_dir = os.path.join('src', 'data')

# set mode as execution parameter
db = DataBase(mode='read', data_path=data_dir)

# create request models
transaction_req_schema = {col: (dtype, None) for col, dtype in np_python_dtype_converter(data_types=db.schema).items()}

transaction_req = create_model('Transaction', **transaction_req_schema)

class Records(BaseModel):
    column: str
    value: Any

# uvicorn src.main:app
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/add_transaction/")
async def add_transaction(req:transaction_req):
    db.insert_transaction(request=dict(req))
    return {
        'date': datetime.now(),
        'message': 'Inserted transaction',
        'request_body': req
    }

@app.post("/search/")
async def search_records(req:Records):
    indexes = db.search_records(**dict(req))
    return {
        'date': datetime.now(),
        'message': 'Searched results',
        'indexes': indexes,
        'request_body': req
    }