from sqlalchemy import Column, Integer, String, Date, DateTime, Float, ForeignKey, Boolean, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False, default='Corretor')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Corretor(Base):
    __tablename__ = 'corretores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(120), unique=True, index=True)
    papel = Column(String(32), default='Corretor')
    ativo = Column(Boolean, default=True)

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome_completo = Column(String(200), index=True)
    cpf_cnpj = Column(String(32), index=True)
    telefone = Column(String(64))
    email = Column(String(120))
    bairro = Column(String(120))
    data_nascimento = Column(Date)
    vidas = Column(Integer, default=1)
    corretor_id = Column(Integer, ForeignKey('corretores.id'))
    data_cadastro = Column(Date)
    categoria = Column(String(64))
    operadora = Column(String(64))
    produto = Column(String(120))
    duracao_meses = Column(Integer)
    numero_contrato = Column(String(64), index=True)
    valor_plano = Column(Float)
    corretor = relationship('Corretor')

class Contrato(Base):
    __tablename__ = 'contratos'
    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    numero_contrato = Column(String(64), unique=True, index=True)
    categoria = Column(String(64))
    operadora = Column(String(64))
    produto = Column(String(120))
    status = Column(String(64))
    valor = Column(Float)
    data_digitacao = Column(Date)
    origem = Column(String(64))
    cliente = relationship('Cliente')

class Comissao(Base):
    __tablename__ = 'comissoes'
    id = Column(Integer, primary_key=True)
    data_pagamento = Column(Date)
    contrato = Column(String(64), index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    corretor_id = Column(Integer, ForeignKey('corretores.id'))
    operadora = Column(String(64))
    valor_bruto = Column(Float)
    descontos = Column(Float, default=0.0)
    valor_liquido = Column(Float)
    parcela = Column(Integer, default=1)
    margem_percentual = Column(Float)
    valor_final = Column(Float)
    log_ref = Column(String(128))
    cliente = relationship('Cliente')
    corretor = relationship('Corretor')

class TabelaMargem(Base):
    __tablename__ = 'tabelas_margem'
    id = Column(Integer, primary_key=True)
    operadora = Column(String(64), index=True)
    categoria = Column(String(64), index=True)
    p1 = Column(Float)
    p2 = Column(Float)
    p3 = Column(Float)
    ativo = Column(Boolean, default=True)
    data_vigencia = Column(Date)
    __table_args__ = (UniqueConstraint('operadora', 'categoria', name='uix_op_cat'),)

class DescontoFixo(Base):
    __tablename__ = 'descontos_fixos'
    id = Column(Integer, primary_key=True)
    operadora = Column(String(64), index=True)
    taxa = Column(Float, default=0.0)
    ativo = Column(Boolean, default=True)

class AuditLog(Base):
    __tablename__ = 'auditoria_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(64))
    entity = Column(String(64))
    entity_id = Column(String(64))
    detail = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
