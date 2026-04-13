"""Add contributions column to projects

Revision ID: d5e6f7a8b9c4
Revises: c4d5e6f7a8b9
Create Date: 2026-04-13 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'd5e6f7a8b9c4'
down_revision = 'c4d5e6f7a8b9'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contributions', sa.ARRAY(sa.String()), nullable=True))


def downgrade():
    with op.batch_alter_table('projects', schema=None) as batch_op:
        batch_op.drop_column('contributions')
