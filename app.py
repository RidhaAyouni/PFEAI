from flask import Flask, redirect, url_for, request, flash, render_template, session
from config import Config
from extensions import db, migrate
from routes.auth import auth_bp
from models.job_app import JobApp
from models.resume import Resume
import os
from models.user import User
from ocr_utils import extract_text_with_layout_pdfplumber


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
                    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
                    resume.save(resume_path)

                    # Perform OCR on the resume
                    extracted_text = extract_text_with_layout_pdfplumber(resume_path)

                    # Save the extracted text to a text file
                    text_file_path = os.path.splitext(resume_path)[0] + '.txt'
                    with open(text_file_path, 'w', encoding='utf-8') as text_file:
                        text_file.write(extracted_text)

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
        user = User.query.filter_by(id=session.get('user_id')).first()  # Assuming you store user's id in session
        return render_template('personal_info.html', user=user)
    
    @app.route('/update_personal_info', methods=['GET', 'POST'])
    def update_personal_info():
        # Retrieve the user's information from the database
        user_id = session.get('user_id')
        user = User.query.get(user_id)

        if request.method == 'POST':
            # Update user information based on the form data
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            user.email = request.form.get('email')

            # Commit the changes to the database
            db.session.commit()

            flash('Personal information updated successfully', 'success')
            return redirect(url_for('personal_info'))

        # Render the template with the user's information pre-filled in the form
        return render_template('update_personal_info.html', user=user)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
