from flask import Flask, redirect, url_for, request, flash, render_template
from config import Config
from extensions import db, migrate
from routes.auth import auth_bp
from models.job_app import JobApp
from models.resume import Resume
import os

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    @app.route('/job_app', methods=['GET', 'POST'])
    def job_app():
        if request.method == 'POST':
            job_title = request.form.get('job_title')
            job_description = request.form.get('job_description')
            requirements = request.form.get('requirements')
            location = request.form.get('location')
            salary_range = request.form.get('salary_range')

            new_job = JobApp(
                job_title=job_title,
                job_description=job_description,
                requirements=requirements,
                location=location,
                salary_range=salary_range
            )

            db.session.add(new_job)
            db.session.commit()
            flash('Job application submitted successfully!', 'success')
            return redirect(url_for('job_app'))

        return render_template('job_app.html')

    @app.route('/job_list')
    def job_list():
        job_apps = JobApp.query.all()
        return render_template('job_list.html', job_apps=job_apps)

    @app.route('/upload_resume', methods=['GET', 'POST'])
    def upload_resume():
        job_apps = JobApp.query.all()
        job_names = [job.job_title for job in job_apps]

        if request.method == 'POST':
            job_name = request.form.get('job_name')
            resumes = request.files.getlist('resume')

            for resume in resumes:
                if not resume:
                    flash('No file uploaded', 'danger')
                    continue

                if resume and resume.filename.endswith('.pdf'):
                    if not os.path.exists(app.config['UPLOAD_FOLDER']):
                        os.makedirs(app.config['UPLOAD_FOLDER'])
                    resume.save(os.path.join(app.config['UPLOAD_FOLDER'], resume.filename))

                    # Create a new Resume object for each uploaded file and add it to the database
                    new_resume = Resume(job_name=job_name, filename=resume.filename)
                    db.session.add(new_resume)

                else:
                    flash('Invalid file format. Only PDF allowed.', 'danger')

            # Commit all uploaded resumes to the database
            db.session.commit()

            flash('Resumes uploaded successfully', 'success')
            return redirect(url_for('upload_resume'))

        return render_template('upload_resume.html', job_names=job_names)

    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')

    @app.route('/personal_info')
    def personal_info():
        return render_template('personal_info.html')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
