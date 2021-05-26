"""Update Migration

Revision ID: 1e88c5d21178
Revises: 78fe7f7528bb
Create Date: 2020-11-08 10:18:11.489836

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1e88c5d21178'
down_revision = '78fe7f7528bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='manufacturer')
    op.drop_index('phone_number', table_name='manufacturer')
    op.drop_column('manufacturer', 'email')
    op.drop_column('manufacturer', 'phone_number')
    op.drop_column('manufacturer', 'address')
    op.add_column('product_log', sa.Column('saled_on', sa.DateTime(), nullable=False))
    op.alter_column('product_log', 'description',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=255),
               nullable=False)
    op.drop_column('product_log', 'started_on')
    op.drop_column('product_log', 'original_price')
    op.drop_column('product_log', 'ended_on')
    op.drop_column('product_log', 'sale_price')
    op.alter_column('recommended_list', 'description',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=255),
               nullable=False)
    op.add_column('recommended_product', sa.Column('ranking', sa.Numeric(), nullable=False))
    op.drop_column('recommended_product', 'profit_rate')
    op.drop_column('recommended_product', 'max_revenue')
    op.drop_column('recommended_product', 'priority')
    op.drop_column('recommended_product', 'min_quantity')
    op.drop_column('recommended_product', 'sale_price')
    op.drop_column('recommended_product', 'accuracy')
    op.drop_column('recommended_product', 'revenue')
    op.drop_column('recommended_product', 'max_quantity')
    op.drop_column('recommended_product', 'original_price')
    op.drop_column('recommended_product', 'min_revenue')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recommended_product', sa.Column('min_revenue', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('original_price', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('max_quantity', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('revenue', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('accuracy', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('sale_price', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('min_quantity', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('priority', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('max_revenue', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('recommended_product', sa.Column('profit_rate', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.drop_column('recommended_product', 'ranking')
    op.alter_column('recommended_list', 'description',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=255),
               nullable=True)
    op.add_column('product_log', sa.Column('sale_price', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('product_log', sa.Column('ended_on', mysql.DATETIME(), nullable=False))
    op.add_column('product_log', sa.Column('original_price', mysql.DECIMAL(precision=10, scale=0), nullable=False))
    op.add_column('product_log', sa.Column('started_on', mysql.DATETIME(), nullable=False))
    op.alter_column('product_log', 'description',
               existing_type=mysql.VARCHAR(collation='utf8_unicode_ci', length=255),
               nullable=True)
    op.drop_column('product_log', 'saled_on')
    op.add_column('manufacturer', sa.Column('address', mysql.VARCHAR(collation='utf8_unicode_ci', length=255), nullable=False))
    op.add_column('manufacturer', sa.Column('phone_number', mysql.VARCHAR(collation='utf8_unicode_ci', length=255), nullable=False))
    op.add_column('manufacturer', sa.Column('email', mysql.VARCHAR(collation='utf8_unicode_ci', length=255), nullable=False))
    op.create_index('phone_number', 'manufacturer', ['phone_number'], unique=True)
    op.create_index('email', 'manufacturer', ['email'], unique=True)
    # ### end Alembic commands ###