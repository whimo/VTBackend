"""empty message

Revision ID: 9a50923bc3f4
Revises: 98c4fd35316e
Create Date: 2019-09-15 12:18:32.151590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a50923bc3f4'
down_revision = '98c4fd35316e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('section', sa.Column('voted_for_percentage', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('section', 'voted_for_percentage')
    # ### end Alembic commands ###
