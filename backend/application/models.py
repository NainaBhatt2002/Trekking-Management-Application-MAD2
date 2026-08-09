from .database import db

# User Model

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False,)   # admin, staff, trekker
    is_active = db.Column(db.Boolean, default=True)
    phone = db.Column(db.String(15), nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    emergency_contact = db.Column(db.String(15), nullable=True)
    blood_group = db.Column(db.String(5), nullable=True)

    treks = db.relationship("Trek", backref="staff", lazy=True)
    bookings = db.relationship("Booking", backref="user", lazy=True)
    
    
# Trek Model

class Trek(db.Model):
    __tablename__ = "treks"
    
    id = db.Column(db.Integer, primary_key=True)
    trek_name = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    trek_date = db.Column(db.Date, nullable=True)
    available_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="Open")
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    
    bookings = db.relationship("Booking", backref="trek", lazy=True)


# Booking Model

class Booking(db.Model):
    __tablename__ = "bookings"
    
    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "trek_id",
            name="unique_user_trek_booking"
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    booking_status = db.Column(db.String(20), default="Booked")   # Booked, Cancelled, Completed
    booking_date = db.Column(db.Date)
    payment_status = db.Column(db.String(20), default="Pending")
    
    
# Staff Profile Model

class StaffProfile(db.Model):
    __tablename__ = "staff_profile"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    experience = db.Column(db.Integer)

    user = db.relationship("User",backref=db.backref("staff_profile", uselist=False))



