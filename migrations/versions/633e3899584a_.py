"""empty message

Revision ID: 633e3899584a
Revises: fed9df350b43
Create Date: 2024-06-03 21:18:08.679287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '633e3899584a'
down_revision = 'fed9df350b43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'skills',
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('skill_name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('skill_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skills')