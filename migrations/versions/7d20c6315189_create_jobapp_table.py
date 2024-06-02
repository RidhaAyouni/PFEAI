"""Create JobApp table

Revision ID: 7d20c6315189
Revises: 69c65fc23da7
Create Date: 2024-06-01 18:58:33.438848

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d20c6315189'
down_revision = '69c65fc23da7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_app',
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('job_title', sa.String(length=100), nullable=False),
    sa.Column('job_description', sa.Text(), nullable=False),
    sa.Column('requirements', sa.Text(), nullable=False),
    sa.Column('location', sa.String(length=100), nullable=False),
    sa.Column('salary_range', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('job_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job_app')
    # ### end Alembic commands ###