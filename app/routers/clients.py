from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Cliente
from ..schemas import ClienteIn, ClienteOut
from ..deps import get_current_user

router = APIRouter(prefix="/clients", tags=["clients"])

@router.get("/", response_model=List[ClienteOut])
def list_clients(q: str | None = Query(default=None), skip: int = 0, limit: int = 50, db: Session = Depends(get_db), _=Depends(get_current_user)):
    qs = db.query(Cliente)
    if q:
        like = f"%{q}%"
        qs = qs.filter(Cliente.nome_completo.like(like))
    return qs.offset(skip).limit(min(limit, 100)).all()

@router.post("/", response_model=ClienteOut)
def create_client(data: ClienteIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    obj = Cliente(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
