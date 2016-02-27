"""empty message

Revision ID: 40f86f562dc2
Revises: bb9f4aba7446
Create Date: 2016-02-26 20:52:14.236720

"""

# revision identifiers, used by Alembic.
revision = '40f86f562dc2'
down_revision = 'bb9f4aba7446'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    ### end Alembic commands ###
