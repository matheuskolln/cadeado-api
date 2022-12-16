"""Add tables

Revision ID: 866ee202650c
Revises: 
Create Date: 2022-12-16 14:29:29.880156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '866ee202650c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('serviceUUID', sa.String(), nullable=False),
    sa.Column('characteristicUUID', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('smartphone_name', sa.String(), nullable=False),
    sa.Column('esp_name', sa.String(), nullable=False),
    sa.Column('esp_mac', sa.String(), nullable=False),
    sa.Column('datetime', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('logs')
    op.drop_table('users')
    # ### end Alembic commands ###