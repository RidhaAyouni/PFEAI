"""empty message

Revision ID: 4c6fa3ced93f
Revises: 6a84b8ca5209
Create Date: 2024-06-03 21:10:52.446482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c6fa3ced93f'
down_revision = '6a84b8ca5209'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'educations',
        sa.Column('education_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), sa.ForeignKey('resumes.id')),
        sa.Column('degree', sa.String(length=255), nullable=False),
        sa.Column('institution_name', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('field_of_study', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('education_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('educations')