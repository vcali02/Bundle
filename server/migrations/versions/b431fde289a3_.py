"""empty message

Revision ID: b431fde289a3
Revises: 2474c602b719
Create Date: 2024-01-08 18:35:59.621906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b431fde289a3'
down_revision = '2474c602b719'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_quantity', sa.Integer(), nullable=False))
        batch_op.drop_column('product_quntity')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('inventories', schema=None) as batch_op:
        batch_op.add_column(sa.Column('product_quntity', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('product_quantity')

    # ### end Alembic commands ###
