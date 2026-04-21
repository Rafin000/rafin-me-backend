"""Add email and reset code columns to users

Revision ID: 8b4f1e9c2d3a
Revises: 7a8f3d2e1c5b
Create Date: 2026-04-21 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b4f1e9c2d3a'
down_revision = 'd5e6f7a8b9c4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('reset_code_hash', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('reset_code_expires_at', sa.DateTime(), nullable=True))
        batch_op.create_unique_constraint('uq_users_email', ['email'])


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint('uq_users_email', type_='unique')
        batch_op.drop_column('reset_code_expires_at')
        batch_op.drop_column('reset_code_hash')
        batch_op.drop_column('email')
