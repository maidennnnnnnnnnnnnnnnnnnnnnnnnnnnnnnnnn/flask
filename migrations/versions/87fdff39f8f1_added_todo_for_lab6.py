"""added todo for lab6

Revision ID: 87fdff39f8f1
Revises: 982afa8a4d3e
Create Date: 2023-11-15 17:18:05.719544

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87fdff39f8f1'
down_revision = '982afa8a4d3e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todo')
    # ### end Alembic commands ###
