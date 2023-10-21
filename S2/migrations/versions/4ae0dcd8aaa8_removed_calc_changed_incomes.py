"""Removed calc, changed Incomes

Revision ID: 4ae0dcd8aaa8
Revises: 1658e72ef5a4
Create Date: 2023-10-21 17:45:58.971930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ae0dcd8aaa8'
down_revision = '1658e72ef5a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('incomes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('incomes', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###
