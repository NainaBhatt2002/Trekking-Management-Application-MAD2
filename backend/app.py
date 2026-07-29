from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User, Trek, Booking, StaffProfile
from werkzeug.security import generate_password_hash
from application.security import jwt

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.routes import *

if __name__ == "__main__":
    db.create_all()
    
    admin = User.query.filter_by(username="admin").first()
    
    if admin is None:
        admin = User(
            username = "admin",
            name = "Administrator",
            email = "admin@gmail.com",
            password = generate_password_hash("admin123"),
            role = "admin"
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("Admin created successfully.")
    
    app.run(debug=True)
