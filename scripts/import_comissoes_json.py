import json
import argparse
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import SessionLocal
from app.models import Comissao, Cliente, Corretor

def parse_date(s):
    if not s:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            pass
    return None

def main(path: str):
    db: Session = SessionLocal()
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for row in data:
        contrato = str(row.get("contrato") or row.get("Número do Contrato") or '').strip()
        cliente_nome = row.get("cliente") or row.get("Nome Completo") or ''
        corretor_nome = row.get("corretor") or row.get("Corretor Responsável") or ''

        cliente = db.query(Cliente).filter(Cliente.numero_contrato == contrato).first()
        if not cliente and cliente_nome:
            cliente = db.query(Cliente).filter(Cliente.nome_completo == cliente_nome).first()

        corretor = db.query(Corretor).filter(Corretor.nome == corretor_nome).first()
        if not corretor and corretor_nome:
            corretor = Corretor(nome=corretor_nome)
            db.add(corretor)
            db.flush()

        valor_bruto = float(str(row.get("valor_bruto") or row.get("Valor do Plano") or 0).replace(',', '.'))
        descontos = float(str(row.get("descontos") or 0).replace(',', '.'))
        valor_liquido = float(str(row.get("valor_liquido") or (valor_bruto - descontos)).replace(',', '.'))
        parcela = int(row.get("parcela") or 1)
        margem_percentual = float(str(row.get("margem_percentual") or 0).replace(',', '.'))
        valor_final = float(str(row.get("valor_final") or (valor_liquido * margem_percentual)).replace(',', '.'))

        obj = Comissao(
            data_pagamento=parse_date(row.get("data_pagamento")),
            contrato=contrato,
            cliente_id=cliente.id if cliente else None,
            corretor_id=corretor.id if corretor else None,
            operadora=row.get("operadora") or (cliente.operadora if cliente else None),
            valor_bruto=valor_bruto,
            descontos=descontos,
            valor_liquido=valor_liquido,
            parcela=parcela,
            margem_percentual=margem_percentual,
            valor_final=valor_final,
            log_ref=row.get("log_ref") or '',
        )
        db.add(obj)
    db.commit()
    db.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--path', required=True)
    args = p.parse_args()
    main(args.path)
