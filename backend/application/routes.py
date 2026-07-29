from flask import current_app as app, jsonify, request
from .models import User
from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, current_user


@app.route("/login", methods=["POST"])
def login():
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    
    user = User.query.filter(
        (User.username == login) | (User.email == login)
    ).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify("Wrong credentials"), 401
    
    access_token = create_access_token(identity=str(user.id))
    return jsonify(
        access_token=access_token, 
        role=user.role
    )

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    
    if not username or not name or not email or not password:
        return jsonify("All fields are required"), 400
    
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        return jsonify("Account already exists"), 409
    
    user = User(
        username=username,
        name=name,
        email=email,
        password=generate_password_hash(password),
        role="trekker"
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify("Registration successful, Happy trekking!"), 201    

@app.route("/profile")
@jwt_required()
def profile():
    return jsonify({
        "message": "You are logged in",
    })
    
@app.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():
    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403
    return jsonify({
        "message": "Welcome to the admin dashboard!"
    }), 200
    
@app.route("/staff/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():
    if current_user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403
    return jsonify({
        "message": "Welcome to the staff dashboard!"
    }), 200
    
@app.route("/trekker/dashboard", methods=["GET"])
@jwt_required()
def trekker_dashboard():
    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403
    return jsonify({
        "message": "Welcome to the trekker dashboard!"
    }), 200
