from extensions import db

class CandidateLanguage(db.Model):
    __tablename__ = 'candidate_languages'

    candidate_language_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.language_id'), nullable=False)
    proficiency_level = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<CandidateLanguage {self.candidate_language_id}>"
