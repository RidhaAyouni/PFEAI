# models/resume.py

from extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(120), nullable=False)
    filename = db.Column(db.String(100))  # To store multiple resume file paths

    def __repr__(self):
        return f'<Resume {self.job_name}>'
