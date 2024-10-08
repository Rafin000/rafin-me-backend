"""image_link column added in Testimonials

Revision ID: b7869912064f
Revises: d577c4b4e416
Create Date: 2024-08-26 13:06:14.323445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7869912064f'
down_revision = 'd577c4b4e416'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('testimonials', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_link', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('testimonials', schema=None) as batch_op:
        batch_op.drop_column('image_link')

    # ### end Alembic commands ###
