"""empty message

Revision ID: 0388b6717e53
Revises: b16d3b335080
Create Date: 2019-08-04 00:43:20.171817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0388b6717e53'
down_revision = 'b16d3b335080'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('photopath', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'photopath')
    # ### end Alembic commands ###
