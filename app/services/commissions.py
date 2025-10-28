from sqlalchemy.orm import Session
from ..models import TabelaMargem, DescontoFixo

PME_OPERADORAS_03 = {"Amil", "Assim", "Bradesco", "SulAmerica", "Porto Seguro", "Klini", "GNDI"}
CORRETORES_ESPECIAIS_30 = {"Camila Adão", "Diogo Lima"}

def _margem_percentual(db: Session, categoria: str, operadora: str, parcela: int, corretor_nome: str) -> float:
    cat = (categoria or '').upper()
    op = (operadora or '').strip()

    if cat.startswith("PME") and any(opx in op for opx in PME_OPERADORAS_03):
        return 0.30
    if cat.startswith("PME") and corretor_nome in CORRETORES_ESPECIAIS_30:
        return 0.30

    row = db.query(TabelaMargem).filter(TabelaMargem.operadora == op, TabelaMargem.categoria == cat, TabelaMargem.ativo == True).first()
    if not row:
        return 0.0
    if parcela == 1:
        return row.p1 or 0.0
    if parcela == 2:
        return row.p2 or 0.0
    return row.p3 or 0.0

def _desconto_fixo(db: Session, operadora: str) -> float:
    row = db.query(DescontoFixo).filter(DescontoFixo.operadora == operadora, DescontoFixo.ativo == True).first()
    return (row.taxa if row else 0.0)

def calcular_comissao(db: Session, *, contrato: str, categoria: str, operadora: str, valor_bruto: float, parcela: int, corretor_nome: str) -> dict:
    m = _margem_percentual(db, categoria, operadora, parcela, corretor_nome)
    desconto = _desconto_fixo(db, operadora)
    valor_liquido = max(valor_bruto - (valor_bruto * desconto), 0.0)
    valor_final = valor_liquido * m
    return {
        "margem_percentual": m,
        "desconto": desconto,
        "valor_liquido": round(valor_liquido, 2),
        "valor_final": round(valor_final, 2),
    }
