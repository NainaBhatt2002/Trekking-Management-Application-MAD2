class Config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///TMS.db"
    JWT_SECRET_KEY = "trekkify-super-secret-key-2026-MAD2Project"