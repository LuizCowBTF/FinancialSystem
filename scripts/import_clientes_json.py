import json
import argparse
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Cliente, Corretor

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
        corretor_nome = row.get("Corretor Responsável") or row.get("Corretor") or ""
        corretor = db.query(Corretor).filter(Corretor.nome == corretor_nome).first()
        if not corretor and corretor_nome:
            corretor = Corretor(nome=corretor_nome)
            db.add(corretor)
            db.flush()

        obj = Cliente(
            nome_completo=row.get("Nome Completo") or row.get("Cliente"),
            cpf_cnpj=row.get("CPF/CNPJ"),
            telefone=row.get("Telefone") or row.get("Telefone 2"),
            email=row.get("Email"),
            bairro=row.get("Bairro"),
            data_nascimento=parse_date(row.get("Data de Nascimento (DD/MM/AAAA)")),
            vidas=int(row.get("Vidas") or 1),
            corretor_id=corretor.id if corretor else None,
            data_cadastro=parse_date(row.get("Data de Cadastro (DD/MM/AAAA)")),
            categoria=row.get("Categoria"),
            operadora=row.get("Operadora"),
            produto=row.get("Produto"),
            duracao_meses=int(row.get("Duração do Contrato (Meses)") or 0) or None,
            numero_contrato=row.get("Número do Contrato") or row.get("Nº CONTRATO"),
            valor_plano=float(str(row.get("Valor do Plano") or row.get("VALOR ORÇAMENTO") or 0).replace(',', '.')),
        )
        db.add(obj)
    db.commit()
    db.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--path', required=True)
    args = p.parse_args()
    main(args.path)
