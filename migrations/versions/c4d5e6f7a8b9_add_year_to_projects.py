"""Add year column to projects

Revision ID: c4d5e6f7a8b9
Revises: b3c4d5e6f7a8
Create Date: 2026-04-13 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c4d5e6f7a8b9'
down_revision = 'b3c4d5e6f7a8'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('year', sa.String(length=255), nullable=True))


def downgrade():
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('year')
