"""empty message

Revision ID: 13ce32da08b3
Revises: 5b01f83de2b5
Create Date: 2019-10-28 09:59:53.249829

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '13ce32da08b3'
down_revision = '5b01f83de2b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'kk')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('kk', mysql.VARCHAR(collation='utf8mb4_bin', length=1000), nullable=True))
    # ### end Alembic commands ###
