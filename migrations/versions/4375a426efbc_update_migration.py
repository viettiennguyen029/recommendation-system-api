"""Update Migration

Revision ID: 4375a426efbc
Revises: 067c732e43eb
Create Date: 2020-11-10 15:18:56.543706

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4375a426efbc'
down_revision = '067c732e43eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_log', sa.Column('recorded_date', sa.DateTime(), nullable=False))
    op.drop_column('product_log', 'ended_on')
    op.drop_column('product_log', 'started_on')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_log', sa.Column('started_on', mysql.DATETIME(), nullable=False))
    op.add_column('product_log', sa.Column('ended_on', mysql.DATETIME(), nullable=False))
    op.drop_column('product_log', 'recorded_date')
    # ### end Alembic commands ###
