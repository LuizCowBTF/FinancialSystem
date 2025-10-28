from alembic import op
import sqlalchemy as sa

revision = '0001_base'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(32), nullable=False, server_default='Corretor'),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('1')),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.UniqueConstraint('email')
    )

    op.create_table('corretores',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome', sa.String(120), nullable=False),
        sa.Column('papel', sa.String(32), server_default='Corretor'),
        sa.Column('ativo', sa.Boolean(), server_default=sa.text('1')),
        sa.UniqueConstraint('nome')
    )

    op.create_table('clientes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('nome_completo', sa.String(200)),
        sa.Column('cpf_cnpj', sa.String(32)),
        sa.Column('telefone', sa.String(64)),
        sa.Column('email', sa.String(120)),
        sa.Column('bairro', sa.String(120)),
        sa.Column('data_nascimento', sa.Date()),
        sa.Column('vidas', sa.Integer(), server_default='1'),
        sa.Column('corretor_id', sa.Integer(), sa.ForeignKey('corretores.id')),
        sa.Column('data_cadastro', sa.Date()),
        sa.Column('categoria', sa.String(64)),
        sa.Column('operadora', sa.String(64)),
        sa.Column('produto', sa.String(120)),
        sa.Column('duracao_meses', sa.Integer()),
        sa.Column('numero_contrato', sa.String(64)),
        sa.Column('valor_plano', sa.Float()),
        sa.Index('ix_clientes_numero_contrato', 'numero_contrato')
    )

    op.create_table('contratos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('cliente_id', sa.Integer(), sa.ForeignKey('clientes.id')),
        sa.Column('numero_contrato', sa.String(64)),
        sa.Column('categoria', sa.String(64)),
        sa.Column('operadora', sa.String(64)),
        sa.Column('produto', sa.String(120)),
        sa.Column('status', sa.String(64)),
        sa.Column('valor', sa.Float()),
        sa.Column('data_digitacao', sa.Date()),
        sa.Column('origem', sa.String(64)),
        sa.UniqueConstraint('numero_contrato'),
        sa.Index('ix_contratos_numero_contrato', 'numero_contrato')
    )

    op.create_table('tabelas_margem',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('operadora', sa.String(64)),
        sa.Column('categoria', sa.String(64)),
        sa.Column('p1', sa.Float()),
        sa.Column('p2', sa.Float()),
        sa.Column('p3', sa.Float()),
        sa.Column('ativo', sa.Boolean(), server_default=sa.text('1')),
        sa.Column('data_vigencia', sa.Date()),
        sa.UniqueConstraint('operadora', 'categoria', name='uix_op_cat')
    )

    op.create_table('descontos_fixos',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('operadora', sa.String(64)),
        sa.Column('taxa', sa.Float(), server_default='0'),
        sa.Column('ativo', sa.Boolean(), server_default=sa.text('1'))
    )

    op.create_table('comissoes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('data_pagamento', sa.Date()),
        sa.Column('contrato', sa.String(64)),
        sa.Column('cliente_id', sa.Integer(), sa.ForeignKey('clientes.id')),
        sa.Column('corretor_id', sa.Integer(), sa.ForeignKey('corretores.id')),
        sa.Column('operadora', sa.String(64)),
        sa.Column('valor_bruto', sa.Float()),
        sa.Column('descontos', sa.Float(), server_default='0'),
        sa.Column('valor_liquido', sa.Float()),
        sa.Column('parcela', sa.Integer(), server_default='1'),
        sa.Column('margem_percentual', sa.Float(), server_default='0'),
        sa.Column('valor_final', sa.Float()),
        sa.Column('log_ref', sa.String(128)),
        sa.Index('ix_comissoes_contrato', 'contrato')
    )

    op.create_table('auditoria_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id')),
        sa.Column('action', sa.String(64)),
        sa.Column('entity', sa.String(64)),
        sa.Column('entity_id', sa.String(64)),
        sa.Column('detail', sa.Text()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    op.drop_table('auditoria_logs')
    op.drop_table('comissoes')
    op.drop_table('descontos_fixos')
    op.drop_table('tabelas_margem')
    op.drop_table('contratos')
    op.drop_table('clientes')
    op.drop_table('corretores')
    op.drop_table('users')
