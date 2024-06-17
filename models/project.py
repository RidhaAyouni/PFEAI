from extensions import db

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    project_title = db.Column(db.String(255), nullable=False)
    project_description = db.Column(db.Text, nullable=False)
    technologies_used = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # Nullable if project is ongoing

    def __repr__(self):
        return f"<Project {self.project_title}>"
