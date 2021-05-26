"""Update migration

Revision ID: 61cb20d5d047
Revises: 417495976685
Create Date: 2021-01-30 21:12:07.172539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '61cb20d5d047'
down_revision = '417495976685'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction_list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('total_amount', sa.Numeric(), nullable=False),
    sa.Column('transaction_list_date', sa.DateTime(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction_list_item',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('transaction_list_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_price', sa.Numeric(), nullable=False),
    sa.Column('quantity', sa.Numeric(), nullable=False),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.Column('updated_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['transaction_list_id'], ['transaction_list.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('invoice')
    op.drop_table('transaction')
    op.add_column('recommended_list', sa.Column('time_span', sa.DateTime(), nullable=False))
    op.add_column('recommended_list', sa.Column('title', sa.String(length=255), nullable=False))
    op.add_column('recommended_list', sa.Column('total_products', sa.Numeric(), nullable=False))
    op.drop_index('name', table_name='recommended_list')
    op.create_unique_constraint(None, 'recommended_list', ['title'])
    op.drop_column('recommended_list', 'ended_on')
    op.drop_column('recommended_list', 'started_on')
    op.drop_column('recommended_list', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recommended_list', sa.Column('name', mysql.VARCHAR(collation='utf8_unicode_ci', length=255), nullable=False))
    op.add_column('recommended_list', sa.Column('started_on', mysql.DATETIME(), nullable=False))
    op.add_column('recommended_list', sa.Column('ended_on', mysql.DATETIME(), nullable=False))
    op.drop_constraint(None, 'recommended_list', type_='unique')
    op.create_index('name', 'recommended_list', ['name'], unique=True)
    op.drop_column('recommended_list', 'total_products')
    op.drop_column('recommended_list', 'title')
    op.drop_column('recommended_list', 'time_span')
    op.create_table('transaction',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('invoice_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('product_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('product_price', mysql.DECIMAL(precision=10, scale=0), nullable=False),
    sa.Column('quantity', mysql.DECIMAL(precision=10, scale=0), nullable=False),
    sa.Column('amount', mysql.DECIMAL(precision=10, scale=0), nullable=False),
    sa.Column('created_on', mysql.DATETIME(), nullable=False),
    sa.Column('updated_on', mysql.DATETIME(), nullable=False),
    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], name='transaction_ibfk_1'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='transaction_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8_unicode_ci',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('invoice',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('customer_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('total_amount', mysql.DECIMAL(precision=10, scale=0), nullable=False),
    sa.Column('invoice_date', mysql.DATETIME(), nullable=False),
    sa.Column('created_on', mysql.DATETIME(), nullable=False),
    sa.Column('updated_on', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8_unicode_ci',
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_table('transaction_list_item')
    op.drop_table('transaction_list')
    # ### end Alembic commands ###