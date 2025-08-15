import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql://root:password@localhost/ec_db?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
