"""Add Product and Webhook tables

Revision ID: 4126546d84c3
Revises: 
Create Date: 2025-11-14 19:57:22.127843

"""
from alembic import op
import sqlalchemy as sa


revision = '4126546d84c3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sku', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.create_index('ix_product_sku_lower', [sa.literal_column('lower(sku)')], unique=True)

    op.create_table('webhook',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=500), nullable=False),
    sa.Column('event_type', sa.String(length=100), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('webhook')
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_index('ix_product_sku_lower')

    op.drop_table('product')
