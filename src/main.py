from fastapi import FastAPI
from pydantic import BaseModel

class Transaction(BaseModel):
    amount: float
    description: str | None

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/transactions/")
def add_transaction(transaction:Transaction):
    return transaction