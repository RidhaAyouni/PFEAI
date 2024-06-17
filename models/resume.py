from extensions import db


class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(120), nullable=False)
    filename = db.Column(db.String(100))
    text_file_path = db.Column(db.String(100))
    ocr_text = db.Column(db.Text)
    processing_status = db.Column(db.String(20))

    def __repr__(self):
        return f'<Resume id={self.id}, job_name={self.job_name}>'
