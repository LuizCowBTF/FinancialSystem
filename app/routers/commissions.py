from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Comissao, Cliente, Corretor
from ..schemas import ComissaoIn, ComissaoOut
from ..deps import get_current_user
from ..services.commissions import calcular_comissao

router = APIRouter(prefix="/commissions", tags=["commissions"])

@router.post("/calc", response_model=ComissaoOut)
def calc_and_store(data: ComissaoIn, db: Session = Depends(get_db), _=Depends(get_current_user)):
    cliente = db.query(Cliente).filter(Cliente.id == data.cliente_id).first() if data.cliente_id else None
    corretor = db.query(Corretor).filter(Corretor.id == data.corretor_id).first() if data.corretor_id else None
    cat = (cliente.categoria if cliente else None) or ""
    op = (cliente.operadora if cliente else None) or (data.operadora or "")

    res = calcular_comissao(
        db,
        contrato=data.contrato,
        categoria=cat,
        operadora=op,
        valor_bruto=data.valor_bruto,
        parcela=data.parcela,
        corretor_nome=(corretor.nome if corretor else ""),
    )

    obj = Comissao(
        contrato=data.contrato,
        cliente_id=data.cliente_id,
        corretor_id=data.corretor_id,
        operadora=op,
        valor_bruto=data.valor_bruto,
        descontos=res["desconto"],
        valor_liquido=res["valor_liquido"],
        parcela=data.parcela,
        margem_percentual=res["margem_percentual"],
        valor_final=res["valor_final"],
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
