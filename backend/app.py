from flask import Flask
from flask_cors import CORS
from application.config import LocalDevelopmentConfig
from application.database import db
from application.models import User, Trek, Booking, StaffProfile
from werkzeug.security import generate_password_hash
from application.security import jwt

app = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    CORS(app, origins=["http://localhost:5173"])
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
        
#Temporary staff creation since admin will create staff users in the future milestone.    
    staff = User.query.filter_by(username="staff").first()

    if staff is None:
        staff = User(
            username="staff",
            name="Test Staff",
            email="staff@gmail.com",
            password=generate_password_hash("staff123"),
            role="staff"
        )

        db.session.add(staff)
        db.session.commit()

    app.run(debug=True)
