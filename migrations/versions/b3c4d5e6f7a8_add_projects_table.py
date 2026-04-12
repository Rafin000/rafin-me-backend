"""Add projects table

Revision ID: b3c4d5e6f7a8
Revises: 7a8f3d2e1c5b
Create Date: 2024-09-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b3c4d5e6f7a8'
down_revision = '7a8f3d2e1c5b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('tech_stack', sa.ARRAY(sa.String), nullable=True),
        sa.Column('github_link', sa.String, nullable=True),
        sa.Column('live_link', sa.String, nullable=True),
        sa.Column('thumbnail_url', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('projects')
