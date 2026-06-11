"""add vendor model and link to product

Revision ID: 5e91760ad143
Revises: 30bec40af061
Create Date: 2026-06-12 01:11:24.679394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e91760ad143'
down_revision = '30bec40af061'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('vendors',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product') as batch_op:
        batch_op.add_column(sa.Column('vendor_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_product_vendor_id', 'vendors', ['vendor_id'], ['id'])


def downgrade():
    with op.batch_alter_table('product') as batch_op:
        batch_op.drop_constraint('fk_product_vendor_id', type_='foreignkey')
        batch_op.drop_column('vendor_id')
    op.drop_table('vendors')
