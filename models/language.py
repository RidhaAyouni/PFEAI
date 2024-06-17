from extensions import db

class Language(db.Model):
    __tablename__ = 'languages'

    language_id = db.Column(db.Integer, primary_key=True)
    language_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Language {self.language_name}>"
