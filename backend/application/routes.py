from flask import current_app as app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from sqlalchemy import func
from .models import User, Trek, Booking

#Authetication routes for login, register and profile

@app.route("/login", methods=["POST"])
def login():
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    
    user = User.query.filter(
        (User.username == login) | (User.email == login)
    ).first()
    
    if (
        not user
        or not user.is_active
        or not check_password_hash(user.password, password)
    ):
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
    
    
#ADMIN DASHBOARD ROUTES

@app.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    recent_bookings = (
        db.session.query(
            Booking.id,
            User.name,
            Trek.trek_name,
            Booking.booking_status,
        )
        .join(User, Booking.user_id == User.id)
        .join(Trek, Booking.trek_id == Trek.id)
        .order_by(Booking.id.desc())
        .limit(5)
        .all()
    )

    return jsonify({
        "total_treks": Trek.query.count(),
        "total_users": User.query.filter_by(role="trekker").count(),
        "total_staff": User.query.filter_by(role="staff").count(),
        "total_bookings": Booking.query.count(),
        "recentBookings": [
            {
                "id": booking.id,
                "user": booking.name,
                "trek": booking.trek_name,
                "status": booking.booking_status,
            }
            for booking in recent_bookings
        ]
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

@app.route("/admin/treks", methods=["GET"])
@jwt_required()
def get_treks():

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    treks = Trek.query.all()

    return jsonify([
        {
            "id": trek.id,
            "trek_name": trek.trek_name,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "staff": trek.staff.name
        }
        for trek in treks
    ])
    
@app.route("/admin/treks", methods=["POST"])
@jwt_required()
def create_trek():

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    trek = Trek(
        trek_name=data["trek_name"],
        difficulty=data["difficulty"],
        duration=data["duration"],
        available_slots=data["available_slots"],
        status=data["status"],
        staff_id=data["staff_id"]
    )

    db.session.add(trek)
    db.session.commit()

    return jsonify({"message": "Trek created successfully"}), 201
    
@app.route("/admin/treks/<int:id>", methods=["PUT"])
@jwt_required()
def update_trek(id):

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get_or_404(id)

    data = request.get_json()

    trek.trek_name = data["trek_name"]
    trek.difficulty = data["difficulty"]
    trek.duration = data["duration"]
    trek.available_slots = data["available_slots"]
    trek.staff_id = data["staff_id"]
    trek.status = data["status"]

    db.session.commit()

    return jsonify({"message": "Trek updated successfully"}), 200

@app.route("/admin/treks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_trek(id):

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get_or_404(id)

    db.session.delete(trek)
    db.session.commit()

    return jsonify({
        "message": "Trek deleted successfully"
    }), 200

@app.route("/admin/staff", methods=["GET"])
@jwt_required()
def get_staff():

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    staff = User.query.filter_by(role="staff").all()

    return jsonify([
        {
            "id": member.id,
            "name": member.name,
            "username": member.username,
            "email": member.email,
            "is_active": member.is_active
        }
        for member in staff
    ])
    
@app.route("/admin/staff", methods=["POST"])
@jwt_required()
def create_staff():

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    existing = User.query.filter(
        (User.username == data["username"]) |
        (User.email == data["email"])
    ).first()

    if existing:
        return jsonify({"message": "User already exists"}), 409

    staff = User(
        name=data["name"],
        username=data["username"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        role="staff"
    )

    db.session.add(staff)
    db.session.commit()

    return jsonify({"message": "Staff created successfully"}), 201

@app.route("/admin/staff/<int:id>", methods=["PUT"])
@jwt_required()
def update_staff(id):

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    staff = User.query.get_or_404(id)

    if staff.role != "staff":
        return jsonify({"message": "Invalid user"}), 400

    data = request.get_json()

    existing = User.query.filter(
        ((User.username == data["username"]) |
         (User.email == data["email"])) &
        (User.id != id)
    ).first()

    if existing:
        return jsonify({"message": "Username or email already exists"}), 409

    staff.name = data["name"]
    staff.username = data["username"]
    staff.email = data["email"]

    if data.get("password"):
        staff.password = generate_password_hash(data["password"])

    db.session.commit()

    return jsonify({
        "message": "Staff updated successfully"
    }), 200

@app.route("/admin/staff/<int:id>/status", methods=["PUT"])
@jwt_required()
def toggle_staff_status(id):

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    staff = User.query.get_or_404(id)

    if staff.role != "staff":
        return jsonify({"message": "Invalid user"}), 400

    staff.is_active = not staff.is_active

    db.session.commit()

    return jsonify({
        "message": "Staff status updated successfully"
    }), 200

@app.route("/admin/users", methods=["GET"])
@jwt_required()
def get_users():

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    users = User.query.filter_by(role="trekker").all()

    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active
        }
        for user in users
    ])
    
@app.route("/admin/users/<int:id>/status", methods=["PUT"])
@jwt_required()
def toggle_user_status(id):

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get_or_404(id)

    if user.role != "trekker":
        return jsonify({"message": "Invalid user"}), 400

    user.is_active = not user.is_active

    db.session.commit()

    return jsonify({
        "message": "User status updated successfully"
    }), 200
    
@app.route("/admin/bookings", methods=["GET"])
@jwt_required()
def get_bookings():

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    bookings = (
        db.session.query(
            Booking.id,
            User.name.label("user_name"),
            User.email,
            Trek.trek_name,
            Booking.booking_date,
            Booking.booking_status,
            Booking.payment_status,
        )
        .join(User, Booking.user_id == User.id)
        .join(Trek, Booking.trek_id == Trek.id)
        .order_by(Booking.id.desc())
        .all()
    )

    return jsonify([
        {
            "id": booking.id,
            "user": booking.user_name,
            "email": booking.email,
            "trek": booking.trek_name,
            "booking_date": booking.booking_date,
            "booking_status": booking.booking_status,
            "payment_status": booking.payment_status,
        }
        for booking in bookings
    ])
    
@app.route("/admin/reports", methods=["GET"])
@jwt_required()
def reports():

    if current_user.role != "admin":
            return jsonify({"message": "Access denied"}), 403

    popular_treks = (
    db.session.query(
        Trek.trek_name,
        func.count(Booking.id).label("bookings")
    )
    .outerjoin(Booking, Trek.id == Booking.trek_id)
    .group_by(Trek.id)
    .order_by(func.count(Booking.id).desc())
    .limit(5)
    .all()
    )

    recent_bookings = (
        db.session.query(
            Booking.id,
            User.name,
            Trek.trek_name,
            Booking.booking_date,
            Booking.booking_status,
        )
        .join(User, Booking.user_id == User.id)
        .join(Trek, Booking.trek_id == Trek.id)
        .order_by(Booking.id.desc())
        .limit(5)
        .all()
    )

    return jsonify({

        "summary": {
            "total_treks": Trek.query.count(),
            "total_users": User.query.filter_by(role="trekker").count(),
            "total_staff": User.query.filter_by(role="staff").count(),
            "total_bookings": Booking.query.count(),
        },

        "trek_status": {
            "Open": Trek.query.filter_by(status="Open").count(),
            "Closed": Trek.query.filter_by(status="Closed").count(),
        },

        "difficulty": {
            "Easy": Trek.query.filter_by(difficulty="Easy").count(),
            "Moderate": Trek.query.filter_by(difficulty="Moderate").count(),
            "Hard": Trek.query.filter_by(difficulty="Hard").count(),
        },

        "users": {
            "Active": User.query.filter_by(
                role="trekker",
                is_active=True
            ).count(),

            "Inactive": User.query.filter_by(
                role="trekker",
                is_active=False
            ).count(),
        },

        "staff": {
            "Active": User.query.filter_by(
                role="staff",
                is_active=True
            ).count(),

            "Inactive": User.query.filter_by(
                role="staff",
                is_active=False
            ).count(),
        },

        "booking_status": {
            "Pending": Booking.query.filter_by(
                booking_status="Pending"
            ).count(),

            "Confirmed": Booking.query.filter_by(
                booking_status="Confirmed"
            ).count(),

            "Cancelled": Booking.query.filter_by(
                booking_status="Cancelled"
            ).count(),
        },

        "payment_status": {
            "Paid": Booking.query.filter_by(
                payment_status="Paid"
            ).count(),

            "Pending": Booking.query.filter_by(
                payment_status="Pending"
            ).count(),
        },

        "popular_treks": [
            {
                "trek_name": trek.trek_name,
                "bookings": trek.bookings
            }
            for trek in popular_treks
        ],

        "recent_bookings": [
            {
                "id": booking.id,
                "user": booking.name,
                "trek": booking.trek_name,
                "date": booking.booking_date,
                "status": booking.booking_status,
            }
            for booking in recent_bookings
        ]

    })
