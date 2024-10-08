"""skills table added

Revision ID: db7fa9c1158b
Revises: b98020cc10fb
Create Date: 2024-08-21 17:01:54.027059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db7fa9c1158b'
down_revision = 'b98020cc10fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_skills',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('skill', sa.String(length=255), nullable=False),
    sa.Column('icon_link', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_skills')
    # ### end Alembic commands ###
