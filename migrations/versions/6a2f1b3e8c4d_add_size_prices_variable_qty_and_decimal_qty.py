"""add size prices, variable qty, decimal quantity

Revision ID: 6a2f1b3e8c4d
Revises: 69436821702c
Create Date: 2026-06-18 02:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = '6a2f1b3e8c4d'
down_revision = '69436821702c'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('shopyo_ecommerce_product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_variable_qty', sa.Boolean(), nullable=False, server_default=sa.text('0')))
        batch_op.add_column(sa.Column('unit_label', sa.String(length=20), nullable=False, server_default='ml'))
        batch_op.add_column(sa.Column('unit_step', sa.Numeric(10, 2), nullable=False, server_default=sa.text('1.0')))

    with op.batch_alter_table('shopyo_ecommerce_size', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Numeric(10, 2), nullable=True))

    with op.batch_alter_table('shopyo_ecommerce_transaction_items', schema=None) as batch_op:
        batch_op.alter_column('quantity', type_=sa.Numeric(10, 2), existing_type=sa.Integer())


def downgrade():
    with op.batch_alter_table('shopyo_ecommerce_transaction_items', schema=None) as batch_op:
        batch_op.alter_column('quantity', type_=sa.Integer(), existing_type=sa.Numeric(10, 2))

    with op.batch_alter_table('shopyo_ecommerce_size', schema=None) as batch_op:
        batch_op.drop_column('price')

    with op.batch_alter_table('shopyo_ecommerce_product', schema=None) as batch_op:
        batch_op.drop_column('unit_step')
        batch_op.drop_column('unit_label')
        batch_op.drop_column('is_variable_qty')
