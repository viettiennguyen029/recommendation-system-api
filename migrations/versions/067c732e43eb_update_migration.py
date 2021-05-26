"""Update Migration

Revision ID: 067c732e43eb
Revises: 1e88c5d21178
Create Date: 2020-11-09 11:58:33.122278

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '067c732e43eb'
down_revision = '1e88c5d21178'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_log', sa.Column('ended_on', sa.DateTime(), nullable=False))
    op.add_column('product_log', sa.Column('original_price', sa.Numeric(), nullable=False))
    op.add_column('product_log', sa.Column('sale_price', sa.Numeric(), nullable=False))
    op.add_column('product_log', sa.Column('started_on', sa.DateTime(), nullable=False))
    op.drop_column('product_log', 'saled_on')
    op.drop_column('product_log', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_log', sa.Column('description', mysql.VARCHAR(collation='utf8_unicode_ci', length=255), nullable=False))
    op.add_column('product_log', sa.Column('saled_on', mysql.DATETIME(), nullable=False))
    op.drop_column('product_log', 'started_on')
    op.drop_column('product_log', 'sale_price')
    op.drop_column('product_log', 'original_price')
    op.drop_column('product_log', 'ended_on')
    # ### end Alembic commands ###