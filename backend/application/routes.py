from flask import current_app as app, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from sqlalchemy import func
from .models import User, Trek, Booking
from sqlalchemy import or_
from datetime import date, datetime
from flask import send_file
from application.tasks import export_trekking_history
from application.celery_app import celery
from celery.result import AsyncResult
import os
import json
from flask_mail import Message
from application.email import mail
from application.cache import (
    redis_client,
    get_cache,
    set_cache,
    delete_cache,
    clear_trek_cache,
    clear_cache_pattern
)

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
            "staff": trek.staff.name if trek.staff else "Unassigned",
            "location": trek.location,
            "trek_date": trek.trek_date.isoformat() if trek.trek_date else None
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
        staff_id=data["staff_id"],
        location=data["location"],
        trek_date=date.fromisoformat(data["trek_date"]) if data.get("trek_date") else None
    )
    db.session.add(trek)
    db.session.commit()
    clear_trek_cache()

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
    trek.location = data["location"]
    trek.trek_date = date.fromisoformat(data["trek_date"]) if data.get("trek_date") else None

    db.session.commit()
    clear_trek_cache()

    return jsonify({"message": "Trek updated successfully"}), 200

@app.route("/admin/treks/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_trek(id):

    if current_user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get_or_404(id)

    db.session.delete(trek)
    db.session.commit()
    clear_trek_cache()

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

    from sqlalchemy.orm import aliased

    StaffUser = aliased(User)

    bookings = (
        db.session.query(
            Booking.id,
            User.name.label("user_name"),
            User.email,
            Trek.trek_name,
            Trek.location,
            Trek.difficulty,
            Trek.duration,
            Trek.trek_date,
            Trek.status.label("trek_status"),
            StaffUser.name.label("staff_name"),
            Booking.booking_date,
            Booking.booking_status,
            Booking.payment_status,
        )
        .join(User, Booking.user_id == User.id)
        .join(Trek, Booking.trek_id == Trek.id)
        .join(StaffUser, Trek.staff_id == StaffUser.id)
        .order_by(Booking.id.desc())
        .all()
    )
    return jsonify([
        {
            "id": booking.id,
            "user": booking.user_name,
            "email": booking.email,
            "trek": booking.trek_name,
            "location": booking.location,
            "difficulty": booking.difficulty,
            "duration": booking.duration,
            "trek_date": booking.trek_date.isoformat() if booking.trek_date else None,
            "trek_status": booking.trek_status,
            "staff": booking.staff_name,
            "booking_date": booking.booking_date,
            "booking_status": booking.booking_status,
            "payment_status": booking.payment_status,
        }
        for booking in bookings
    ]), 200
    
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
            "Booked": Booking.query.filter_by(
                booking_status="Booked"
            ).count(),

            "Completed": Booking.query.filter_by(
                booking_status="Completed"
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
    

#STAFF DASHBOARD ROUTES

@app.route("/staff/dashboard", methods=["GET"])
@jwt_required()
def staff_dashboard():

    if current_user.role != "staff":
        return jsonify({"message": "Access denied"}), 403

    assigned_treks = Trek.query.filter_by(staff_id=current_user.id).all()

    total_assigned = len(assigned_treks)

    open_treks = sum(
        1 for trek in assigned_treks
        if trek.status == "Open"
    )

    started_treks = sum(
        1 for trek in assigned_treks
        if trek.status == "Started"
    )

    completed_treks = sum(
        1 for trek in assigned_treks
        if trek.status == "Completed"
    )

    registered_trekkers = (
        db.session.query(func.count(Booking.id))
        .join(Trek)
        .filter(Trek.staff_id == current_user.id)
        .scalar()
    )

    return jsonify({
        "assigned_treks": total_assigned,
        "registered_trekkers": registered_trekkers,
        "open_treks": open_treks,
        "started_treks": started_treks,
        "completed_treks": completed_treks
    }), 200

@app.route("/staff/treks", methods=["GET"])
@jwt_required()
def get_staff_treks():

    if current_user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    cache_key = f"staff:treks:{current_user.id}"

    cached = get_cache(cache_key)

    if cached:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached), 200

    print(f"CACHE MISS: {cache_key}")

    treks = Trek.query.filter_by(
        staff_id=current_user.id
    ).all()

    response_data = [
        {
            "id": trek.id,
            "trek_name": trek.trek_name,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "trek_date": (
                trek.trek_date.isoformat()
                if trek.trek_date else None
            ),
            "available_slots": trek.available_slots,
            "status": trek.status,
            "registered_users": len(trek.bookings),
            "location": trek.location
        }
        for trek in treks
    ]

    set_cache(
        cache_key,
        response_data,
        timeout=60
    )

    return jsonify(response_data), 200
    
@app.route("/staff/treks/<int:id>", methods=["GET"])
@jwt_required()
def get_staff_trek(id):

    if current_user.role != "staff":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get_or_404(id)

    if trek.staff_id != current_user.id:
        return jsonify({"message": "Forbidden"}), 403

    return jsonify({
        "id": trek.id,
        "trek_name": trek.trek_name,
        "difficulty": trek.difficulty,
        "duration": trek.duration,
        "trek_date": trek.trek_date.isoformat() if trek.trek_date else None,
        "available_slots": trek.available_slots,
        "status": trek.status,
        "location": trek.location
    }), 200
    
@app.route("/staff/treks/<int:id>", methods=["PUT"])
@jwt_required()
def update_staff_trek(id):

    if current_user.role != "staff":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get_or_404(id)

    if trek.staff_id != current_user.id:
        return jsonify({"message": "Forbidden"}), 403

    data = request.get_json()

    if data["available_slots"] < 0:
        return jsonify({
            "message": "Available slots cannot be negative."
        }), 400

    trek.available_slots = data["available_slots"]
    trek.status = data["status"]

    db.session.commit()
    
    clear_trek_cache()
    
    delete_cache(
        f"staff:treks:{current_user.id}"
    )

    return jsonify({
        "message": "Trek updated successfully"
    }), 200
    
@app.route("/staff/treks/<int:id>/participants", methods=["GET"])
@jwt_required()
def get_participants(id):

    if current_user.role != "staff":
        return jsonify({"message": "Access denied"}), 403

    trek = Trek.query.get_or_404(id)

    if trek.staff_id != current_user.id:
        return jsonify({"message": "Forbidden"}), 403

    bookings = (
        db.session.query(
            Booking.id,
            User.name,
            User.email,
            Booking.booking_status,
            Booking.booking_date
        )
        .join(User, Booking.user_id == User.id)
        .filter(Booking.trek_id == id)
        .all()
    )

    return jsonify([
        {
            "booking_id": booking.id,
            "name": booking.name,
            "email": booking.email,
            "booking_status": booking.booking_status,
            "booking_date": booking.booking_date,
            "location": trek.location
        }

        for booking in bookings
    ]), 200
    
@app.route("/staff/bookings", methods=["PUT"])
@jwt_required()
def update_booking_status():

    if current_user.role != "staff":
        return jsonify({
            "message": "Access denied"
        }), 403

    data = request.get_json()

    affected_users = set()

    for item in data:

        booking = Booking.query.get(item["booking_id"])

        if not booking:
            continue

        trek = Trek.query.get(booking.trek_id)

        if trek.staff_id != current_user.id:
            return jsonify({
                "message": "Unauthorized"
            }), 403

        booking.booking_status = item["booking_status"]

        affected_users.add(booking.user_id)

    db.session.commit()

    for user_id in affected_users:

        delete_cache(
            f"dashboard:trekker:{user_id}"
        )

        delete_cache(
            f"bookings:trekker:{user_id}"
        )

    return jsonify({
        "message": "Booking statuses updated successfully."
    }), 200

#TREKKER DASHBOARD ROUTES

@app.route("/trekker/dashboard", methods=["GET"])
@jwt_required()
def trekker_dashboard():

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    cache_key = f"dashboard:trekker:{current_user.id}"

    cached = get_cache(cache_key)

    if cached:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached), 200

    print(f"CACHE MISS: {cache_key}")

    available_treks = Trek.query.filter(
        Trek.status == "Open",
        Trek.available_slots > 0
    ).count()

    booked_treks = Booking.query.filter_by(
        user_id=current_user.id
    ).count()

    completed_treks = Booking.query.join(Trek).filter(
        Booking.user_id == current_user.id,
        Trek.status == "Completed"
    ).count()

    pending_bookings = Booking.query.filter(
        Booking.user_id == current_user.id,
        Booking.booking_status == "Pending"
    ).count()

    cancelled_bookings = Booking.query.filter(
        Booking.user_id == current_user.id,
        Booking.booking_status == "Cancelled"
    ).count()

    recent_bookings = (
        Booking.query
        .filter_by(user_id=current_user.id)
        .order_by(Booking.id.desc())
        .limit(5)
        .all()
    )

    response_data = {
        "available_treks": available_treks,
        "booked_treks": booked_treks,
        "completed_treks": completed_treks,
        "pending_bookings": pending_bookings,
        "cancelled_bookings": cancelled_bookings,

        "recentBookings": [
            {
                "id": booking.id,
                "trek": booking.trek.trek_name,
                "location": booking.trek.location,
                "trek_date": booking.trek.trek_date.isoformat() if booking.trek.trek_date else None,
                "booking_status": booking.booking_status,
                "trek_status": booking.trek.status,
                "date": booking.booking_date.isoformat() if booking.booking_date else None
            }
            for booking in recent_bookings
        ]
    }

    set_cache(
        cache_key,
        response_data,
        timeout=30
    )

    return jsonify(response_data), 200
    
@app.route("/trekker/treks", methods=["GET"])
@jwt_required()
def get_available_treks():

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")
    duration = request.args.get("duration", type=int)
    location = request.args.get("location", "")

    # create a unique cache key for each filter combination
    cache_key = (
        f"treks:"
        f"search={search}:"
        f"difficulty={difficulty}:"
        f"duration={duration}:"
        f"location={location}"
    )

    # check Redis cache
    cached_treks = redis_client.get(cache_key)

    if cached_treks:
        print("CACHE HIT:", cache_key)

        return jsonify(
            json.loads(cached_treks)
        ), 200

    print("CACHE MISS:", cache_key)

    query = Trek.query.filter(
        Trek.status == "Open"
    )

    if search:
        query = query.filter(
            Trek.trek_name.ilike(f"%{search}%")
        )

    if difficulty:
        query = query.filter(
            Trek.difficulty == difficulty
        )

    if duration:
        query = query.filter(
            Trek.duration == duration
        )

    if location:
        query = query.filter(
            Trek.location.ilike(f"%{location}%")
        )

    treks = query.all()

    trek_data = [
        {
            "id": trek.id,
            "trek_name": trek.trek_name,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "trek_date": (
                trek.trek_date.isoformat()
                if trek.trek_date
                else None
            ),
            "available_slots": trek.available_slots,
            "status": trek.status,
            "location": trek.location
        }
        for trek in treks
    ]

    #store result in Redis for 60 seconds
    redis_client.set(
        cache_key,
        json.dumps(trek_data),
        ex=60
    )

    return jsonify(trek_data), 200
   
@app.route("/trekker/treks/<int:id>", methods=["GET"])
@jwt_required()
def get_trek_details(id):

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    cache_key = f"trek:details:{id}"

    cached = get_cache(cache_key)

    if cached:
        print(f"CACHE HIT: {cache_key}")
        existing_booking = Booking.query.filter_by(
            user_id=current_user.id,
            trek_id=id
        ).first()
        cached["is_booked"] = existing_booking is not None
        return jsonify(cached), 200

    print(f"CACHE MISS: {cache_key}")

    trek = Trek.query.get_or_404(id)

    response_data = {
        "id": trek.id,
        "trek_name": trek.trek_name,
        "location": trek.location,
        "difficulty": trek.difficulty,
        "duration": trek.duration,
        "available_slots": trek.available_slots,
        "status": trek.status
    }

    set_cache(
        cache_key,
        response_data,
        timeout=60
    )

    # Check if current user already booked this trek
    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=id
    ).first()

    response_data["is_booked"] = existing_booking is not None

    return jsonify(response_data), 200

@app.route("/trekker/bookings/<int:id>", methods=["POST"])
@jwt_required()
def book_trek(id):

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    trek = Trek.query.get_or_404(id)

    if trek.status != "Open":
        return jsonify({
            "message": "This trek is closed."
        }), 400

    if trek.available_slots <= 0:
        return jsonify({
            "message": "No slots available."
        }), 400

    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=id
    ).first()

    if existing_booking:
        return jsonify({
            "message": "You have already booked this trek."
        }), 400

    booking = Booking(
        user_id=current_user.id,
        trek_id=id,
        booking_status="Booked",
        booking_date=date.today(),
        payment_status="Pending"
    )

    db.session.add(booking)
    trek.available_slots -= 1
    db.session.commit()
    
    clear_trek_cache()

    delete_cache(
        f"dashboard:trekker:{current_user.id}"
    )

    delete_cache(
        f"bookings:trekker:{current_user.id}"
    )

    return jsonify({
        "message": "Trek booked successfully."
    }), 201
    
@app.route("/trekker/bookings", methods=["GET"])
@jwt_required()
def get_my_bookings():

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    cache_key = f"bookings:trekker:{current_user.id}"

    cached = get_cache(cache_key)

    if cached:
        print(f"CACHE HIT: {cache_key}")
        return jsonify(cached), 200

    print(f"CACHE MISS: {cache_key}")

    bookings = (
        Booking.query
        .filter_by(user_id=current_user.id)
        .order_by(Booking.booking_date.desc())
        .all()
    )

    response_data = [
        {
            "id": booking.id,
            "trek_name": booking.trek.trek_name,
            "location": booking.trek.location,
            "difficulty": booking.trek.difficulty,
            "duration": booking.trek.duration,
            "booking_status": booking.booking_status,
            "trek_date": (
                booking.trek.trek_date.isoformat()
                if booking.trek.trek_date else None
            ),
            "trek_status": booking.trek.status,
            "booking_date": (
                booking.booking_date.isoformat()
                if booking.booking_date else None
            )
        }
        for booking in bookings
    ]

    set_cache(
        cache_key,
        response_data,
        timeout=30
    )

    return jsonify(response_data), 200
    
@app.route("/trekker/profile", methods=["GET"])
@jwt_required()
def get_profile():

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "name": current_user.name,
        "email": current_user.email,
        "phone": current_user.phone,
        "gender": current_user.gender,
        "age": current_user.age,
        "address": current_user.address,
        "emergency_contact": current_user.emergency_contact,
        "blood_group": current_user.blood_group
    }), 200
    
@app.route("/trekker/profile", methods=["PUT"])
@jwt_required()
def update_profile():

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    data = request.get_json()
    data = request.get_json()

    current_user.name = data["name"]
    current_user.email = data["email"]
    current_user.phone = data.get("phone")
    current_user.gender = data.get("gender")
    current_user.age = data.get("age")
    current_user.address = data.get("address")
    current_user.emergency_contact = data.get("emergency_contact")
    current_user.blood_group = data.get("blood_group")
    
    import re

    email = data["email"].strip()

    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return jsonify({
            "message": "Please enter a valid email address."
        }), 400

    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully."
    }), 200
    
@app.route("/trekker/export-history", methods=["POST"])
@jwt_required()
def start_trekking_history_export():

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    task = export_trekking_history.delay(
        current_user.id
    )

    return jsonify({
        "message": "Export started.",
        "task_id": task.id
    }), 202
    
@app.route("/trekker/export-history/status/<task_id>", methods=["GET"])
@jwt_required()
def export_history_status(task_id):

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    task = AsyncResult(
        task_id,
        app=celery
    )

    if task.state == "PENDING":

        return jsonify({
            "status": "Processing"
        }), 200

    if task.state == "SUCCESS":

        result = task.result

        if result["user_id"] != current_user.id:
            return jsonify({
                "message": "Access denied"
            }), 403

        return jsonify({
            "status": "Completed",
            "filename": result["filename"]
        }), 200

    if task.state == "FAILURE":

        return jsonify({
            "status": "Failed"
        }), 200

    return jsonify({
        "status": task.state
    }), 200
    
@app.route("/trekker/export-history/download/<task_id>", methods=["GET"])
@jwt_required()
def download_trekking_history(task_id):

    if current_user.role != "trekker":
        return jsonify({
            "message": "Access denied"
        }), 403

    task = AsyncResult(
        task_id,
        app=celery
    )

    if task.state != "SUCCESS":
        return jsonify({
            "message": "Export is not ready yet."
        }), 400

    result = task.result

    if result["user_id"] != current_user.id:
        return jsonify({
            "message": "Access denied"
        }), 403

    if not os.path.exists(result["filepath"]):
        return jsonify({
            "message": "Export file not found."
        }), 404

    return send_file(
        result["filepath"],
        as_attachment=True,
        download_name=result["filename"],
        mimetype="text/csv"
    )
    
    
#temporary route

@app.route("/test-email")
def test_email():
    msg = Message(
        subject="Trekkify Test Email",
        sender="trekkify@localhost",
        recipients=["test@example.com"],
        body="This is a test email from Trekkify."
    )

    mail.send(msg)

    return jsonify({
        "message": "Test email sent successfully."
    }), 200