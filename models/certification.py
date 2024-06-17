from extensions import db

class Certification(db.Model):
    __tablename__ = 'certifications'

    certification_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))
    certification_name = db.Column(db.String(255), nullable=False)
    organization = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Certification {self.certification_name} from {self.organization}>"
