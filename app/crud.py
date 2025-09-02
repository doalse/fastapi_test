from sqlalchemy.orm import Session
from models import Vacancy
from typing import Annotated
from fastapi import Depends, HTTPException, status, Path, Body
from database import get_db
from schemas import VacancyRequest

db_dependency = Annotated[Session, Depends(get_db)]

def read_root(db: db_dependency):
    return db.query(Vacancy).all()

def read_vacancy(db: db_dependency, vacancy_id: int = Path(..., gt=0)):
    model = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
    return model

def create_vacancy(db: db_dependency, vacancy: VacancyRequest):
    model = Vacancy(**vacancy.model_dump())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

def update_vacancy(db: db_dependency, vacancy_id: int = Path(..., gt=0), vacancy: VacancyRequest = Body(...)):
    model = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
    for key, value in vacancy.model_dump().items():
        setattr(model, key, value)
    db.commit()
    return model

def delete_vacancy(db: db_dependency, vacancy_id: int = Path(..., gt=0)):
    model = db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
    db.delete(model)
    db.commit()
    return {"detail": "Vacancy deleted"}