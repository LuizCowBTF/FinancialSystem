from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Contrato
from ..deps import get_current_user

router = APIRouter(prefix="/contracts", tags=["contracts"])

@router.get("/")
def list_contracts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Contrato).offset(skip).limit(min(limit, 100)).all()
