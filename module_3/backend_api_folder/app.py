from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn
from pydantic import Field

load_dotenv()
app = FastAPI(title="Simple FastAPI App", version="1.0.0")
data=[{"name":"John", "age":30, "city":"New York"},
      {"name":"Anna", "age":22, "city":"London"},
      {"name":"Mike", "age":32, "city":"Chicago"},
      {"name":"Sara", "age":27, "city":"San Francisco"}]


class item(BaseModel):
    name: str = Field(..., example="Perpetual")
    city: str = Field(..., example="New York")
    age: int = Field(..., example=30)


@app.get("/", description= "This endpoint just returns a welcome message")
def root():
    return {"Message":"Welcome to my FastAPI Application"}

@app.get("/get_data", description= "This endpoint returns a list of data")
def get_data():
    return data


@app.post("/create_data", description= "This endpoint adds a new item to the data list")
def create_data(req: item):
    data.append(req.dict())
    print(data)
    return {"Message": "Data Received", "Data": data}

@app.put("/update_data/{id}")
def update_data(id:int, req: item):
    data[id] = req.dict()
    print(data)
    return {"Message": "Data Updated", "Data": data}

if __name__ == "__main__":
    print(os.getenv("host"))
    print(os.getenv("port"))
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))
