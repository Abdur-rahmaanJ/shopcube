"""empty message

Revision ID: 11e2212fd0b5
Revises: 6a2f1b3e8c4d
Create Date: 2026-06-30 23:39:56.760219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11e2212fd0b5'
down_revision = '6a2f1b3e8c4d'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('shopyo_ecommerce_product') as batch_op:
        batch_op.alter_column('is_variable_qty',
                   existing_type=sa.BOOLEAN(),
                   nullable=True,
                   existing_server_default=sa.text('0'))
        batch_op.alter_column('unit_label',
                   existing_type=sa.VARCHAR(length=20),
                   nullable=True,
                   existing_server_default=sa.text("'ml'"))
        batch_op.alter_column('unit_step',
                   existing_type=sa.NUMERIC(precision=10, scale=2),
                   nullable=True,
                   existing_server_default=sa.text('(1.0)'))


def downgrade():
    with op.batch_alter_table('shopyo_ecommerce_product') as batch_op:
        batch_op.alter_column('unit_step',
                   existing_type=sa.NUMERIC(precision=10, scale=2),
                   nullable=False,
                   existing_server_default=sa.text('(1.0)'))
        batch_op.alter_column('unit_label',
                   existing_type=sa.VARCHAR(length=20),
                   nullable=False,
                   existing_server_default=sa.text("'ml'"))
        batch_op.alter_column('is_variable_qty',
                   existing_type=sa.BOOLEAN(),
                   nullable=False,
                   existing_server_default=sa.text('0'))
