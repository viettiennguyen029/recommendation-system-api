"""Update migration

Revision ID: 52c1237d3ee0
Revises: 19c78ad5ba82
Create Date: 2021-02-18 10:09:01.254773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52c1237d3ee0'
down_revision = '19c78ad5ba82'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction_list', sa.Column('notes', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction_list', 'notes')
    # ### end Alembic commands ###