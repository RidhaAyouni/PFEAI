from extensions import db
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CandidateSkill(db.Model):
    __tablename__ = 'candidate_skills'

    candidate_skill_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.skill_id'), nullable=False)

    def __repr__(self):
        return f"<CandidateSkill {self.candidate_skill_id}>"
