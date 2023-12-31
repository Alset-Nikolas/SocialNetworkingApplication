"""add date post

Revision ID: d7525c4a2b01
Revises: befd5dd233fa
Create Date: 2023-07-21 22:18:07.535555

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd7525c4a2b01'
down_revision = 'befd5dd233fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_table', sa.Column('date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post_table', 'date')
    # ### end Alembic commands ###
