"""empty message

Revision ID: 4471438b2cae
Revises: 22c29be55dbc
Create Date: 2019-08-30 19:37:46.431567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4471438b2cae'
down_revision = '22c29be55dbc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=150), nullable=False),
    sa.Column('item_name', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cart')
    # ### end Alembic commands ###
