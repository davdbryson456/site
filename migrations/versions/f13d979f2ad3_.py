"""empty message

Revision ID: f13d979f2ad3
Revises: 7f587f2d5bcc
Create Date: 2019-09-03 17:43:59.167353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f13d979f2ad3'
down_revision = '7f587f2d5bcc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('custfname', sa.String(length=150), nullable=False),
    sa.Column('custlname', sa.String(length=150), nullable=False),
    sa.Column('phonenum', sa.String(length=200), nullable=False),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(length=200), nullable=False),
    sa.Column('qty', sa.String(length=200), nullable=False),
    sa.Column('Orders_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['Orders_id'], ['orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_content')
    op.drop_table('orders')
    # ### end Alembic commands ###
