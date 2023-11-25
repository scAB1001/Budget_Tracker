"""init

Revision ID: b2358485bdaf
Revises: 
Create Date: 2023-11-23 15:27:59.594797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2358485bdaf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cars',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('model', sa.String(length=255), nullable=True),
    sa.Column('make', sa.String(length=255), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('body_type', sa.String(length=255), nullable=True),
    sa.Column('monthly_payment', sa.Float(), nullable=True),
    sa.Column('horsepower', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.Column('first_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('leases',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('term_length', sa.Integer(), nullable=True),
    sa.Column('mileage_limit', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_interactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.Column('swipe_type', sa.String(length=10), nullable=True),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_interactions')
    op.drop_table('leases')
    op.drop_table('user')
    op.drop_table('cars')
    # ### end Alembic commands ###
