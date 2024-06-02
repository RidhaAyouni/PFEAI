# models/resume.py

from extensions import db
from sqlalchemy.dialects.postgresql import ARRAY

# class Resume(db.Model):
#     __tablename__ = 'resumes'
#     id = db.Column(db.Integer, primary_key=True)
#     job_name = db.Column(db.String(120), nullable=False)
#     filename = db.Column(db.String(100))  # To store multiple resume file paths
#     # text = db.Column(db.String(1000))
class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(120), nullable=False)
    filename = db.Column(db.String(100))  # To store resume file path
    text_file_path = db.Column(db.String(100))  # To store extracted text file path
    ocr_text = db.Column(db.Text)  # To store OCR extracted text
    processing_status = db.Column(db.String(20))  # To store status (e.g., 'uploaded', 'processed', 'failed')

    def __repr__(self):
        return f'<Resume {self.job_name}>'
