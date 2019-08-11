"""empty message

Revision ID: 34e55647ca49
Revises: 0388b6717e53
Create Date: 2019-08-11 01:07:22.499520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34e55647ca49'
down_revision = '0388b6717e53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accessories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('photopath', sa.String(length=255), nullable=True),
    sa.Column('stock_status', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('new_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bookname', sa.String(length=150), nullable=False),
    sa.Column('author', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('photopath', sa.String(length=255), nullable=True),
    sa.Column('stock_status', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('custname', sa.String(length=150), nullable=False),
    sa.Column('ordernum', sa.Integer(), nullable=True),
    sa.Column('order', sa.String(length=200), nullable=False),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_fname', sa.String(length=100), nullable=False),
    sa.Column('user_lname', sa.String(length=100), nullable=False),
    sa.Column('photopath', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('supplies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('photopath', sa.String(length=255), nullable=True),
    sa.Column('stock_status', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('used_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bookname', sa.String(length=150), nullable=False),
    sa.Column('author', sa.String(length=150), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('photopath', sa.String(length=255), nullable=True),
    sa.Column('stock_status', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=100), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('first_n', sa.String(length=100), nullable=False),
    sa.Column('last_n', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('used_book')
    op.drop_table('supplies')
    op.drop_table('post')
    op.drop_table('orders')
    op.drop_table('new_book')
    op.drop_table('accessories')
    # ### end Alembic commands ###