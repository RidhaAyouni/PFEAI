import os
import pandas as pd
from tqdm import tqdm
import fitz  # PyMuPDF
from extensions import db
from models.resume import Resume
from models.candidate import Candidate
from models.experience import Experience
from models.education import Education
from models.project import Project
from models.certification import Certification
from models.skill import Skill
from models.language import Language

class CVsReader:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def read_cv(self):
        print('---- Executing CVs Content Extraction Process ----')
        df = self._read_pdfs_content_from_directory()
        print('Cleaning CVs Content...')
        df['ocr_text'] = df['ocr_text'].astype(str)
        df['ocr_text'] = df['ocr_text'].str.replace(r"\n(?:\s*)", "\n", regex=True)
        print('CVs Content Extraction Process Completed!')
        print('----------------------------------------------')
        return df

    def _read_pdfs_content_from_directory(self):
        data = {'filename': [], 'ocr_text': []}
        for filename in tqdm(os.listdir(self.directory_path), desc='CVs'):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.directory_path, filename)
                try:
                    content = extract_text_from_pdf(file_path)
                    data['filename'].append(filename)
                    data['ocr_text'].append(content)
                except Exception as e:
                    print(f"Error reading file {filename}: {e}")
        return pd.DataFrame(data)

def extract_text_from_pdf(filepath):
    try:
        document = fitz.open(filepath)
        text = ""
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {filepath}: {e}")
        return None
    
def extract_and_process_cvs(file_paths, job_name):
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    for file_path in file_paths:
        try:
            ocr_text = extract_text_from_pdf(file_path)
            if ocr_text:
                filename = os.path.basename(file_path)
                text_filename = os.path.splitext(filename)[0] + '.txt'
                text_file_path = os.path.join('uploads', text_filename)
                with open(text_file_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(ocr_text)

                new_resume = Resume(
                    filename=filename,
                    job_name=job_name,
                    text_file_path=text_file_path,
                    ocr_text=ocr_text,
                    processing_status='Pending'
                )
                db.session.add(new_resume)
                db.session.commit()
            else:
                print(f"Empty text extracted from {file_path}.")
        except Exception as e:
            print(f"Error processing CV {file_path}: {str(e)}")


def parse_and_save_candidate(candidate_data, resume_id):
    if candidate_data:
        candidate = Candidate(
            first_name=candidate_data.get('first_name', ''),
            last_name=candidate_data.get('last_name', ''),
            email=candidate_data.get('email', ''),
            phone_num=candidate_data.get('phone_num', ''),
            address=candidate_data.get('address', ''),
            date_of_birth=candidate_data.get('date_of_birth', ''),
            resume_id=resume_id
        )
        db.session.add(candidate)
        db.session.commit()

def parse_and_save_experience(experience_data, resume_id):
    if experience_data:
        experience = Experience(
            job_title=experience_data.get('job_title', ''),
            company_name=experience_data.get('company_name', ''),
            start_date=experience_data.get('start_date', ''),
            end_date=experience_data.get('end_date', ''),
            job_description=experience_data.get('job_description', ''),
            resume_id=resume_id
        )
        db.session.add(experience)
        db.session.commit()

def parse_and_save_education(education_data, resume_id):
    if education_data:
        education = Education(
            degree=education_data.get('degree', ''),
            institution_name=education_data.get('institution_name', ''),
            start_date=education_data.get('start_date', ''),
            end_date=education_data.get('end_date', ''),
            field_of_study=education_data.get('field_of_study', ''),
            resume_id=resume_id
        )
        db.session.add(education)
        db.session.commit()

def parse_and_save_projects(project_data, resume_id):
    if project_data:
        project = Project(
            project_title=project_data.get('project_title', ''),
            project_description=project_data.get('project_description', ''),
            technologies_used=project_data.get('technologies_used', ''),
            start_date=project_data.get('start_date', ''),
            end_date=project_data.get('end_date', ''),
            resume_id=resume_id
        )
        db.session.add(project)
        db.session.commit()

def parse_and_save_certifications(certification_data, resume_id):
    if certification_data:
        certification = Certification(
            certification_name=certification_data.get('certification_name', ''),
            organization=certification_data.get('organization', ''),
            issue_date=certification_data.get('issue_date', ''),
            expiration_date=certification_data.get('expiration_date', ''),
            resume_id=resume_id
        )
        db.session.add(certification)
        db.session.commit()

def parse_and_save_skills(skill_data, resume_id):
    if skill_data:
        skill = Skill(
            skill_name=skill_data.get('skill_name', ''),
            proficiency_level=skill_data.get('proficiency_level', ''),
            resume_id=resume_id
        )
        db.session.add(skill)
        db.session.commit()

def parse_and_save_languages(language_data, resume_id):
    if language_data:
        language = Language(
            language_name=language_data.get('language_name', ''),
            proficiency_level=language_data.get('proficiency_level', ''),
            resume_id=resume_id
        )
        db.session.add(language)
        db.session.commit()

