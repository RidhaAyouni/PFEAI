from extensions import db

class Candidate(db.Model):
    __tablename__ = 'candidates'

    candidate_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'))

    def __repr__(self):
        return f"<Candidate {self.first_name} {self.last_name}>"
