import os
import traceback
from flask import Flask, redirect, url_for, request, flash, render_template, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from extensions import db, migrate
from config import Config
from routes.auth import auth_bp
from models.user import User
from models.job_app import JobApp
from models.resume import Resume
from ChatGPT_Pipeline import CVsInfoExtractor
from OCR_Reader import extract_and_process_cvs

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

app = create_app()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/job_app', methods=['GET', 'POST'])
def job_app():
    try:
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
                salary_range=salary_range,
            )

            db.session.add(new_job)
            db.session.commit()
            flash('Job application submitted successfully!', 'success')
            return redirect(url_for('job_list'))

        return render_template('job_app.html')

    except Exception as e:
        flash(f'Error in job application submission: {str(e)}', 'danger')
        print(f"Error in job application submission: {str(e)}")
        traceback.print_exc()
        return redirect(url_for('job_app'))

@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    try:
        job_names = [job.job_title for job in JobApp.query.all()]

        if request.method == 'POST':
            if 'resume' not in request.files:
                flash('No file uploaded', 'danger')
                return redirect(request.url)

            job_name = request.form.get('job_name')
            resumes = request.files.getlist('resume')
            file_paths = []

            for resume in resumes:
                if not resume:
                    flash('No file uploaded', 'danger')
                    continue

                if resume and allowed_file(resume.filename):
                    filename = secure_filename(resume.filename)
                    resume_path_pdf = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    resume.save(resume_path_pdf)
                    file_paths.append(resume_path_pdf)

                    new_resume = Resume(
                        filename=filename,
                        job_name=job_name,
                        text_file_path=resume_path_pdf,
                        processing_status='Pending'
                    )
                    db.session.add(new_resume)
                    db.session.commit()

                    try:
                        extract_and_process_cvs([resume_path_pdf], job_name)
                        flash('Resumes uploaded and processed successfully', 'success')
                    except Exception as e:
                        flash(f'Error during CV processing: {str(e)}', 'danger')
                        print(f"Error during CV processing: {str(e)}")
                        traceback.print_exc()
                else:
                    flash('Invalid file format. Only PDF allowed.', 'danger')

            return redirect(url_for('upload_resume'))

        return render_template('upload_resume.html', job_names=job_names)

    except Exception as e:
        flash(f'Error in resume upload: {str(e)}', 'danger')
        print(f"Error in resume upload: {str(e)}")
        traceback.print_exc()
        return redirect(url_for('upload_resume'))

@app.route('/job_list')
def job_list():
    try:
        job_apps = JobApp.query.all()
        return render_template('job_list.html', job_apps=job_apps)

    except Exception as e:
        flash(f'Error fetching job list: {str(e)}', 'danger')
        print(f"Error fetching job list: {str(e)}")
        traceback.print_exc()
        return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/personal_info')
def personal_info():
    try:
        if 'user_id' not in session:
            flash('Please log in first.', 'danger')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(id=session['user_id']).first()
        return render_template('personal_info.html', user=user)

    except Exception as e:
        flash(f'Error in personal info page: {str(e)}', 'danger')
        print(f"Error in personal info page: {str(e)}")
        traceback.print_exc()
        return redirect(url_for('dashboard'))

@app.route('/update_personal_info', methods=['GET', 'POST'])
def update_personal_info():
    try:
        if 'user_id' not in session:
            flash('Please log in first.', 'danger')
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(id=session['user_id']).first()

        if request.method == 'POST':
            user.first_name = request.form.get('first_name')
            user.last_name = request.form.get('last_name')
            user.email = request.form.get('email')
            user.phone_num = request.form.get('phone_num')
            user.address = request.form.get('address')

            db.session.commit()
            flash('Personal information updated successfully!', 'success')
            return redirect(url_for('personal_info'))

        return render_template('update_personal_info.html', user=user)

    except Exception as e:
        flash(f'Error updating personal info: {str(e)}', 'danger')
        print(f"Error updating personal info: {str(e)}")
        traceback.print_exc()
        return redirect(url_for('update_personal_info'))

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

import json

@app.route('/process_CV', methods=['GET', 'POST'])
def process_CV():
    resumes = Resume.query.filter_by(processing_status='Pending').all()
    print(f"Found {len(resumes)} pending resumes.")  # Debug statement

    if request.method == 'POST':
        for resume in resumes:
            try:
                print(f"Processing resume: {resume.filename}")  # Debug statement

                # Check if OCR text exists
                if not resume.ocr_text:
                    print(f"Empty OCR text extracted from {resume.filename}.")
                    continue  # Skip processing if OCR text is empty

                # Assuming CVsInfoExtractor is correctly imported and instantiated
                extractor = CVsInfoExtractor()  # Adjust this based on your implementation
                json_response = extractor.process_cv(resume)  # Pass the entire Resume object

                # Attempt to parse JSON response
                try:
                    if json_response:
                        parsed_data = json.loads(json_response)
                        # Process parsed_data as needed
                        print("Parsed JSON successfully:", parsed_data)
                    else:
                        print(f"No valid JSON response from {resume.filename}")
                        continue  # Skip to next resume

                except json.JSONDecodeError as e:
                    print(f"Failed to decode JSON response from {resume.filename}. Error: {str(e)}")
                    flash(f'Failed to decode JSON response from {resume.filename}', 'danger')
                    continue  # Skip to next resume

                # Assuming processing logic here

            except Exception as e:
                flash(f'Error processing {resume.filename}: {str(e)}', 'danger')
                print(f"Error processing {resume.filename}: {str(e)}")
                traceback.print_exc()

        return redirect(url_for('process_CV'))

    return render_template('process_CV.html', resumes=resumes)




if __name__ == '__main__':
    app.run(debug=True)
