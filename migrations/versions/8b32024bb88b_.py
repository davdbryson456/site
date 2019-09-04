"""empty message

Revision ID: 8b32024bb88b
Revises: f7cae76ca0a2
Create Date: 2019-08-28 17:34:21.281093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b32024bb88b'
down_revision = 'f7cae76ca0a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('n_title', sa.String(length=255), nullable=False),
    sa.Column('n_Dateposted', sa.DateTime(), nullable=False),
    sa.Column('n_content', sa.Text(), nullable=False),
    sa.Column('userfname', sa.String(length=100), nullable=False),
    sa.Column('userlname', sa.String(length=100), nullable=False),
    sa.Column('photopath', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('news')
    # ### end Alembic commands ###