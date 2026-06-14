"""add location_id to transactions

Revision ID: 1c6f25e61a59
Revises: 2605d15953fa
Create Date: 2026-06-12 19:11:50.318210

"""
from alembic import op
import sqlalchemy as sa


revision = '1c6f25e61a59'
down_revision = '2605d15953fa'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.add_column(sa.Column('location_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_transactions_location_id', 'locations', ['location_id'], ['id'])


def downgrade():
    with op.batch_alter_table('transactions') as batch_op:
        batch_op.drop_constraint('fk_transactions_location_id', type_='foreignkey')
        batch_op.drop_column('location_id')
