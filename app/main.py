from fastapi import FastAPI, Depends, status, Path, Body
from typing import Annotated
from sqlalchemy.orm import Session
import crud
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine, get_db


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

from schemas import VacancyRequest

db_dependency = Annotated[Session, Depends(get_db)]

origins = [
    "http://localhost:5173", #frontend address
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #allow only frontend address
    allow_credentials=True, #allow cookies, authorization headers, etc.S
    allow_methods=["*"], #allow all methods
    allow_headers=["*"],  #allow all headers
)

    
@app.get("/", status_code=status.HTTP_200_OK)
def read_root(db: db_dependency):
    return crud.read_root(db)
  
@app.get("/vacancy/{vacancy_id}", status_code=status.HTTP_200_OK)
def read_vacancy(db: db_dependency, vacancy_id: int = Path(..., gt=0)):
    return crud.read_vacancy(db, vacancy_id)

@app.post("/vacancy", status_code=status.HTTP_201_CREATED)
def create_vacancy(db: db_dependency, vacancy: VacancyRequest):
    return crud.create_vacancy(db, vacancy)

@app.put("/vacancy/{vacancy_id}", status_code=status.HTTP_202_ACCEPTED)
def update_vacancy(db: db_dependency, vacancy_id: int = Path(..., gt=0), vacancy: VacancyRequest = Body(...)):
    return crud.update_vacancy(db, vacancy_id, vacancy)

@app.delete("/vacancy/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacancy(db: db_dependency, vacancy_id: int = Path(..., gt=0)):
    return crud.delete_vacancy(db, vacancy_id)