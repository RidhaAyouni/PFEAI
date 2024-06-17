from extensions import db

class Education(db.Model):
    __tablename__ = 'educations'

    education_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    degree = db.Column(db.String(255), nullable=False)
    institution_name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    field_of_study = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Education {self.degree} at {self.institution_name}>"
