from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    class Config:
        from_attributes = True

class ClienteIn(BaseModel):
    nome_completo: str
    cpf_cnpj: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[EmailStr] = None
    bairro: Optional[str] = None
    data_nascimento: Optional[date] = None
    vidas: int = 1
    corretor_id: Optional[int] = None
    data_cadastro: Optional[date] = None
    categoria: Optional[str] = None
    operadora: Optional[str] = None
    produto: Optional[str] = None
    duracao_meses: Optional[int] = None
    numero_contrato: Optional[str] = None
    valor_plano: Optional[float] = None

class ClienteOut(ClienteIn):
    id: int
    class Config:
        from_attributes = True

class ComissaoIn(BaseModel):
    data_pagamento: Optional[date] = None
    contrato: str
    cliente_id: Optional[int] = None
    corretor_id: Optional[int] = None
    operadora: Optional[str] = None
    valor_bruto: float
    descontos: float = 0.0
    parcela: int = 1
    margem_percentual: float = 0.0

class ComissaoOut(BaseModel):
    id: int
    contrato: str
    valor_liquido: float
    valor_final: float
    parcela: int
    class Config:
        from_attributes = True
