"""empty message

Revision ID: 51f1600db5a4
Revises: 4c6fa3ced93f
Create Date: 2024-06-03 21:13:36.188274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51f1600db5a4'
down_revision = '4c6fa3ced93f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'certifications',
        sa.Column('certification_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), sa.ForeignKey('resumes.id')),
        sa.Column('certification_name', sa.String(length=255), nullable=False),
        sa.Column('organization', sa.String(length=255), nullable=False),
        sa.Column('issue_date', sa.Date(), nullable=False),
        sa.Column('expiration_date', sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint('certification_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('certifications')