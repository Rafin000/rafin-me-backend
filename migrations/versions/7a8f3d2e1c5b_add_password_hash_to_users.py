"""Add password_hash to users

Revision ID: 7a8f3d2e1c5b
Revises: c54b4e4878c5
Create Date: 2026-04-07 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a8f3d2e1c5b'
down_revision = 'c54b4e4878c5'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('password_hash')
