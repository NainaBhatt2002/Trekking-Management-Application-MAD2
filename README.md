Trekking Management Application V2 (MAD-II)

My app, Trekkify, is a Trekking Management Application being developed as part of the **Modern Application Development II (MAD II)** course at IIT Madras.
The application aims to provide a platform for managing trekking activities by connecting administrators, trek staff, and trekkers through a single system.

## Features

* JWT-based authentication and role-based access
* Trek creation and management
* Trek booking and booking management
* Trekker profile and booking history
* Trek Staff dashboard
* Participant management
* Admin and staff dashboards
* Trek slot and status management
* Redis caching
* Celery background tasks
* Celery Beat scheduled tasks
* Frontend and backend validation
* Responsive UI using Bootstrap

## Technology Stack

* Flask	- Backend REST API
* Flask-SQLAlchemy - Database ORM
* SQLite - Database
* Flask-JWT-Extended - JWT authentication
* Flask-CORS - Cross-origin API access
* Vue.js - Frontend
* Vite - Frontend development/build tool
* Axios - API communication
* Bootstrap - UI styling
* Redis / Memurai - Caching and Celery broker
* Celery - Background task processing
* Celery Beat - Scheduled tasks

## Project Structure
TREKKING-MANAGEMENT/
│
├── backend/
│   ├── application/
│   │   ├── celery.py
│   │   ├── celery_app.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── email.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── security.py
│   │   └── tasks.py
│   │
│   ├── instance/
│   ├── app.py
│   ├── celerybeat-schedule
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── assets/
│       ├── components/
│       ├── router/
│       ├── services/
│       ├── views/
│       ├── App.vue
│       └── main.js
│
├── .gitignore
├── package.json
├── package-lock.json
└── README.md

## Author

**Naina Bhatt**
BS Degree in Data Science and Applications
Indian Institute of Technology Madras

-------------------------------------------------------

**MAD 2 Project commands**

Backend Terminal:

* inside backend folder, creating virtual env: python -m venv .venv
* activating virtual env: .\.venv\Scripts\Activate
* pip install Flask Flask-SQLAlchemy Flask-JWT-Extended flask-cors (initially)
* pip install > requirements.txt
* pip install celery redis pandas reportlab (initially)
* pip install > requirements.txt
* Inside backend folder, start app: python app.py


2. Celery Backend Terminal (Bash):

* Inside backend, in .venv, start celery worker: python -m celery -A application.celery_app.celery worker --pool=solo --loglevel=info (in windows always use --pool=solo)
* Similarly, for celery beat: python -m celery -A application.celery_app.celery beat --loglevel=info

3. Frontend Terminal:

* inside frontend folder, install packages(first time only): npm install
* Run vue: npm run dev

4. In another terminal, in backend .venv, to check redis server running, write: memurai-cli ping (E.O. - PONG)

5. In another bash terminal, write the path of MailHog and run it and open it in a browser

6. Git commands:

* Check status: git status
* Stage: git add .
* Commit: git commit -m "Message"
* Push: git push
* Amend last commit: git commit --amend -m "New Message"
* Push amended commit: git push --force-with-lease
* Create Milestone Tag: git tag milestone-1
* Push tag: git push origin milestone-1