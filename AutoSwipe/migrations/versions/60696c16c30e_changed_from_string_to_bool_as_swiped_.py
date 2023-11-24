"""Changed from STRING to BOOL as swiped_right

Revision ID: 60696c16c30e
Revises: b2358485bdaf
Create Date: 2023-11-24 20:06:28.741129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60696c16c30e'
down_revision = 'b2358485bdaf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_interactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('swiped_right', sa.Boolean(), nullable=True))
        batch_op.drop_column('swipe_type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_interactions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('swipe_type', sa.VARCHAR(length=10), nullable=True))
        batch_op.drop_column('swiped_right')

    # ### end Alembic commands ###