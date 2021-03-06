"""empty message

Revision ID: f7cae76ca0a2
Revises: 23c0c71b52ad
Create Date: 2019-08-26 14:21:26.029914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7cae76ca0a2'
down_revision = '23c0c71b52ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('homepage_pics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pic_name', sa.String(length=255), nullable=False),
    sa.Column('caption', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('homepage_pics')
    # ### end Alembic commands ###
