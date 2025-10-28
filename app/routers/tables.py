from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import TabelaMargem, DescontoFixo
from ..deps import require_roles

router = APIRouter(prefix="/tables", tags=["tables"])

@router.get("/margens")
def list_margens(db: Session = Depends(get_db), _=Depends(require_roles("Master", "Adm1"))):
    return db.query(TabelaMargem).all()

@router.post("/margens")
def create_margem(data: dict, db: Session = Depends(get_db), _=Depends(require_roles("Master", "Adm1"))):
    obj = TabelaMargem(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/descontos")
def list_desc(db: Session = Depends(get_db), _=Depends(require_roles("Master", "Adm1"))):
    return db.query(DescontoFixo).all()

@router.post("/descontos")
def create_desc(data: dict, db: Session = Depends(get_db), _=Depends(require_roles("Master", "Adm1"))):
    obj = DescontoFixo(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
