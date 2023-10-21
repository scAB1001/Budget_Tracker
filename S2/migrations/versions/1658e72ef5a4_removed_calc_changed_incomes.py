"""Removed calc, changed Incomes

Revision ID: 1658e72ef5a4
Revises: e74a481bd416
Create Date: 2023-10-21 17:45:15.785669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1658e72ef5a4'
down_revision = 'e74a481bd416'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('calculations')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calculations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('expr', sa.VARCHAR(length=100), nullable=False),
    sa.Column('result', sa.FLOAT(), nullable=False),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('expr')
    )
    # ### end Alembic commands ###
