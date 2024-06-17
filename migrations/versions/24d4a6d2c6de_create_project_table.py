"""Create Project table

Revision ID: 24d4a6d2c6de
Revises: faaa27e4945a
Create Date: 2024-06-03 20:35:41.262576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24d4a6d2c6de'
down_revision = 'faaa27e4945a'
branch_labels = None
depends_on = None


def upgrade():
    # Create the 'projects' table
    op.create_table(
        'projects',
        sa.Column('project_id', sa.Integer(), primary_key=True),
        sa.Column('resume_id', sa.Integer(), sa.ForeignKey('resumes.id')),
        sa.Column('project_title', sa.String(length=255), nullable=False),
        sa.Column('project_description', sa.Text(), nullable=False),
        sa.Column('technologies_used', sa.String(length=255), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
    )


def downgrade():
    # Drop the 'projects' table
    op.drop_table('projects')
