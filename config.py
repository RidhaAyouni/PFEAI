import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:pfe/2024@localhost/AI_PFE')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'D:/code_copies/copy4_ocr/PFE_AI/PFEAI/uploads'
    ALLOWED_EXTENSIONS = {'pdf'}
