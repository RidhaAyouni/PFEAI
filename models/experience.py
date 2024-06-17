from extensions import db

class Experience(db.Model):
    __tablename__ = 'experiences'

    experience_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    job_title = db.Column(db.String(255), nullable=False)
    company_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    job_description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Experience {self.job_title} at {self.company_name}>"
