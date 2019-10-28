"""empty message

Revision ID: 5b01f83de2b5
Revises: 
Create Date: 2019-10-28 09:59:33.462697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b01f83de2b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('article', sa.Column('kk', sa.String(length=1000), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'kk')
    # ### end Alembic commands ###