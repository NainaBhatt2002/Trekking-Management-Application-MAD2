import csv
import os
import requests
from datetime import datetime, date, timedelta
from calendar import monthrange
from sqlalchemy import func
from flask_mail import Message
from application.celery_app import celery
from application.database import db
from application.email import mail
from application.models import User, Trek, Booking


# CSV Export Task

@celery.task
def export_trekking_history(user_id):
    from app import create_app

    app = create_app()

    with app.app_context():
        bookings = (
            Booking.query
            .filter_by(user_id=user_id)
            .order_by(Booking.booking_date.desc())
            .all()
        )

        export_folder = os.path.join(
            app.instance_path,
            "exports"
        )

        os.makedirs(export_folder, exist_ok=True)

        filename = (
            f"trekking_history_{user_id}_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        )

        filepath = os.path.join(
            export_folder,
            filename
        )

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile)

            writer.writerow([
                "Trek Name",
                "Location",
                "Difficulty",
                "Duration",
                "Trek Date",
                "Booking Status",
                "Trek Status"
            ])

            for booking in bookings:
                writer.writerow([
                    booking.trek.trek_name,
                    booking.trek.location,
                    booking.trek.difficulty,
                    booking.trek.duration,
                    booking.trek.trek_date,
                    booking.booking_status,
                    booking.trek.status
                ])

        return {
            "user_id": user_id,
            "filename": filename,
            "filepath": filepath
        }


# Daily Reminder Task

@celery.task
def send_trek_reminders():
    from app import create_app

    app = create_app()

    with app.app_context():
        today = date.today()

        reminder_dates = [
            today + timedelta(days=3),
            today + timedelta(days=2),
            today + timedelta(days=1)
        ]

        treks = Trek.query.filter(
            Trek.trek_date.in_(reminder_dates)
        ).all()

        webhook_url = app.config["GOOGLE_CHAT_WEBHOOK_URL"]

        reminders_sent = 0

        for trek in treks:
            days_left = (trek.trek_date - today).days

            bookings = Booking.query.filter_by(
                trek_id=trek.id,
                booking_status="Booked"
            ).all()

            for booking in bookings:
                user = booking.user

                if days_left == 1:
                    countdown = "🚨 Your trek is tomorrow!"
                else:
                    countdown = f"⏳ {days_left} days left!"

                message = {
                    "text": (
                        f"🏔️ Trekkify Trek Reminder\n\n"
                        f"Hi {user.name}!\n"
                        f"{countdown}\n\n"
                        f"🥾 Trek: {trek.trek_name}\n"
                        f"📍 Location: {trek.location}\n"
                        f"⚡ Difficulty: {trek.difficulty}\n"
                        f"📅 Trek Date: "
                        f"{trek.trek_date.strftime('%d %B %Y')}\n\n"
                        f"Have a great trek! 🌄"
                    )
                }

                try:
                    response = requests.post(
                        webhook_url,
                        json=message,
                        timeout=10
                    )
                    response.raise_for_status()
                    reminders_sent += 1
                except Exception as e:
                    print(f"Failed to send reminder for booking {booking.id}: {e}")

        return {
            "message": "Trek reminders sent successfully.",
            "reminders_sent": reminders_sent
        }
        
        
# Monthly Report Generation Task

@celery.task
def generate_monthly_report():
    from app import create_app

    app = create_app()

    with app.app_context():
        today = date.today()

        if today.month == 1:
            report_month = 12
            report_year = today.year - 1
        else:
            report_month = today.month - 1
            report_year = today.year

        start_date = date(
            report_year,
            report_month,
            1
        )

        end_date = date(
            report_year,
            report_month,
            monthrange(
                report_year,
                report_month
            )[1]
        )

        completed_treks = Trek.query.filter(
            Trek.trek_date >= start_date,
            Trek.trek_date <= end_date,
            Trek.status == "Completed"
        ).all()

        trek_ids = [
            trek.id
            for trek in completed_treks
        ]

        total_participants = 0

        if trek_ids:
            total_participants = Booking.query.filter(
                Booking.trek_id.in_(trek_ids),
                Booking.booking_status == "Completed"
            ).count()

        popular_treks = (
            db.session.query(
                Trek.trek_name,
                func.count(Booking.id).label("participants")
            )
            .join(
                Booking,
                Booking.trek_id == Trek.id
            )
            .filter(
                Trek.trek_date >= start_date,
                Trek.trek_date <= end_date,
                Trek.status == "Completed",
                Booking.booking_status == "Completed"
            )
            .group_by(
                Trek.id,
                Trek.trek_name
            )
            .order_by(
                func.count(Booking.id).desc()
            )
            .limit(5)
            .all()
        )

        popular_html = ""

        for trek_name, participants in popular_treks:
            popular_html += f"""
            <tr>
                <td>{trek_name}</td>
                <td>{participants}</td>
            </tr>
            """

        if not popular_html:
            popular_html = """
            <tr>
                <td colspan="2">
                    No trekking activity recorded.
                </td>
            </tr>
            """

        report_html = f"""
        <html>
        <body style="font-family: Arial; padding: 30px;">

            <h1 style="color:#1677ff;">
                🏔️ Trekkify Monthly Trekking Report
            </h1>

            <p>
                <b>Reporting Period:</b>
                {start_date.strftime("%d %B %Y")}
                -
                {end_date.strftime("%d %B %Y")}
            </p>

            <hr>

            <h2>Monthly Summary</h2>

            <p>
                <b>Treks Conducted:</b>
                {len(completed_treks)}
            </p>

            <p>
                <b>Total Participants:</b>
                {total_participants}
            </p>

            <h2>Popular Treks</h2>

            <table
                border="1"
                cellpadding="10"
                style="border-collapse:collapse; width:100%;"
            >
                <tr>
                    <th>Trek</th>
                    <th>Participants</th>
                </tr>

                {popular_html}

            </table>

            <br>

            <p style="color:#777;">
                This report was automatically generated by Trekkify.
            </p>

        </body>
        </html>
        """

        admin = User.query.filter_by(
            role="admin"
        ).first()

        if not admin:
            return {
                "message": "No admin user found."
            }

        msg = Message(
            subject=(
                f"Trekkify Monthly Report - "
                f"{start_date.strftime('%B %Y')}"
            ),
            recipients=[admin.email],
            html=report_html
        )

        mail.send(msg)

        return {
            "message": "Monthly report sent successfully.",
            "admin_email": admin.email,
            "treks_conducted": len(completed_treks),
            "participants": total_participants
        }