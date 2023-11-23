"""No longer 1-to-m 1-to-m = m-to-m or normalised but simpler now

Revision ID: 523ac16df950
Revises: fdebb4e8414c
Create Date: 2023-11-23 03:45:11.469135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '523ac16df950'
down_revision = 'fdebb4e8414c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_interactions', schema=None) as batch_op:
        batch_op.alter_column('swipe_type',
               existing_type=sa.VARCHAR(length=5),
               type_=sa.String(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_interactions', schema=None) as batch_op:
        batch_op.alter_column('swipe_type',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=5),
               existing_nullable=True)

    # ### end Alembic commands ###
