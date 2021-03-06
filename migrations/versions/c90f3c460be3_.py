"""empty message

Revision ID: c90f3c460be3
Revises: 9c2b28dcf63e
Create Date: 2019-09-08 14:23:15.943324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c90f3c460be3'
down_revision = '9c2b28dcf63e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('three_vids',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('onevidpath3', sa.String(length=255), nullable=True),
    sa.Column('c_name3', sa.String(length=255), nullable=True),
    sa.Column('vid_title3', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('three_vids')
    # ### end Alembic commands ###
