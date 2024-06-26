"""empty message

Revision ID: 761b2f42d59c
Revises: 633e3899584a
Create Date: 2024-06-03 21:20:39.945472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '761b2f42d59c'
down_revision = '633e3899584a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'candidate_languages',
        sa.Column('candidate_language_id', sa.Integer(), nullable=False),
        sa.Column('resume_id', sa.Integer(), nullable=False),
        sa.Column('language_id', sa.Integer(), nullable=False),
        sa.Column('proficiency_level', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['language_id'], ['languages.language_id'], name='fk_candidate_languages_language_id'),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], name='fk_candidate_languages_resume_id'),
        sa.PrimaryKeyConstraint('candidate_language_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('candidate_languages')