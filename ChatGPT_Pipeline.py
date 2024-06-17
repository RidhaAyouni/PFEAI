import os
import json
import openai
import traceback
from datetime import datetime  # Add datetime import

from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager

import config  # Assuming config.py is in the same directory
from models.resume import Resume
from models.candidate import Candidate
from models.education import Education
from models.experience import Experience
from models.skill import Skill
from models.language import Language
from models.candidate_skill import CandidateSkill
from extensions import db
from OCR_Reader import CVsReader  # Assuming ocr_reader.py is in the same directory

# Load environment variables
load_dotenv()

# Define the connection to the database using the configuration settings
DATABASE_URI = config.Config.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Define a directory for uploads (assuming it's defined in config or environment)
UPLOADS_DIR = 'uploads/'

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

class CVsInfoExtractor:
    @staticmethod
    def _call_gpt_for_cv_info_extraction(cv_content, prompt_file='prompt.txt', openai_api_key=os.getenv('OPENAI_API_KEY')):
        try:
            openai.api_key = openai_api_key
            with open(prompt_file, 'r') as file:
                prompt = file.read()

            # Update the call to use ChatCompletion.create
            completion_params = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'system', 'content': prompt},
                    {'role': 'user', 'content': cv_content}
                ],
                'max_tokens': 1500,
            }
            response = openai.ChatCompletion.create(**completion_params)
            if 'choices' in response and len(response['choices']) > 0:
                cleaned_response = response['choices'][0]['message']['content'].strip()
                try:
                    json_response = json.loads(cleaned_response)
                except json.JSONDecodeError:
                    print("Failed to decode JSON response.")
                    print("Raw response:", cleaned_response)
                    json_response = None
            else:
                print("No valid choices in the response.")
                json_response = None
            return json_response
        except Exception as e:
            print(f"Error calling GPT-3 for CV info extraction: {str(e)}")
            traceback.print_exc()
            return None

    @staticmethod
    def _normalize_and_save_to_db(json_response, session, resume_id):
        try:
            print(f"Normalizing and saving to DB: {json_response}")  # Debug statement

            # Extract candidate information
            candidate_info = {
                'first_name': json_response.get('First Name', '').strip(),
                'last_name': json_response.get('Last Name', '').strip(),
                'email': json_response.get('Email/Phone', '').strip(),
                'address': json_response.get('Address', '').strip(),
                'date_of_birth': json_response.get('Date of Birth', '').strip(),
                'resume_id': resume_id
            }

            # Check for mandatory fields
            if not candidate_info['first_name'] or not candidate_info['last_name'] or not candidate_info['email']:
                print("Missing mandatory candidate information, skipping database insertion.")
                return False

            # Create Candidate object and add to session
            candidate = Candidate(**candidate_info)
            session.add(candidate)
            session.commit()

            # Extract and save skills
            skills = json_response.get('Skills', [])
            if isinstance(skills, str):  # Skills might be a string instead of a list
                skills = [s.strip() for s in skills.split(',') if s.strip()]

            for skill_name in skills:
                skill_name = skill_name.strip()
                if skill_name:
                    skill = session.query(Skill).filter_by(name=skill_name).first()
                    if not skill:
                        skill = Skill(name=skill_name)
                        session.add(skill)
                        session.commit()
                    candidate_skill = CandidateSkill(resume_id=resume_id, skill_id=skill.skill_id)
                    session.add(candidate_skill)

            # Extract education information
            education_info = json_response.get('Education', {})
            if education_info:
                education = Education(
                    institution_name=education_info.get('Institution Name', '').strip(),
                    degree=education_info.get('Degree', '').strip(),
                    field_of_study=education_info.get('Field of Study', '').strip(),
                    start_date=education_info.get('Start Date', '').strip(),
                    end_date=education_info.get('End Date', '').strip(),
                    resume_id=resume_id
                )
                session.add(education)

            # Extract experience information
            experience_info = json_response.get('Experience', {})
            if experience_info:
                experience = Experience(
                    job_title=experience_info.get('Job Title', '').strip(),
                    company_name=experience_info.get('Company Name', '').strip(),
                    start_date=experience_info.get('Start Date', '').strip(),
                    end_date=experience_info.get('End Date', '').strip(),
                    job_description=experience_info.get('Job Description', '').strip(),
                    resume_id=resume_id
                )
                session.add(experience)

            session.commit()  # Commit all changes at once
            return True
        except Exception as e:
            print(f"Error processing CV and saving to database: {str(e)}")
            traceback.print_exc()
            session.rollback()  # Rollback changes if an error occurs
            return False

    @staticmethod
    def process_cv(resume):
        try:
            cv_content = resume.ocr_text
            print(cv_content)
            if cv_content:

                json_response = CVsInfoExtractor._call_gpt_for_cv_info_extraction(cv_content)
                if json_response:
                    # Parse Date of Birth from JSON response
                    date_str = json_response.get('Date of Birth', '').strip()
                    date_of_birth = datetime.strptime(date_str, '%Y-%m-%d') if date_str and date_str != 'N/A' else None
                    json_response['Date of Birth'] = date_of_birth  # Update date_of_birth in json_response

                    with session_scope() as session:
                        success = CVsInfoExtractor._normalize_and_save_to_db(json_response, session, resume.id)
                        return success
                else:
                    print("No valid JSON response from GPT-3.")
                    return False
            else:
                print(f"Empty OCR text extracted from {resume.filename}.")
                return False
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            print("Raw response:", cv_content)  # Print the original content for debugging
            return False
        except Exception as e:
            print(f"Error processing CV: {str(e)}")
            traceback.print_exc()
            return False
