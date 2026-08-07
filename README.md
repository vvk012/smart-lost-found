# Smart Lost & Found Portal for College Campus

A centralized web application for students to report, search, and recover
lost/found items on campus. Built with Flask, SQLAlchemy, and Bootstrap 5.
Aligned with **SDG 11: Sustainable Cities and Communities** — reducing waste
and building trust-based community infrastructure on campus.

## Tech Stack
- Backend: Python, Flask (application factory + blueprints)
- Frontend: HTML5, CSS3, Bootstrap 5, vanilla JavaScript
- Database: SQLite
- ORM: SQLAlchemy (via Flask-SQLAlchemy)
- Auth: Flask-Login + Flask-Bcrypt (password hashing)
- Forms/Security: Flask-WTF (CSRF protection, server-side validation)

## Setup Instructions

1. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS/Linux
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Initialize the database and default admin account:
   ```
   python seed.py
   ```
   This creates `database/lostfound.db` and an admin login:
   - username: `admin`
   - password: `admin123`
   (Change this before showing the project to anyone else.)

4. Run the application:
   ```
   flask --app app run --debug
   ```
   or
   ```
   python app.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

## Project Structure

```
smart-lost-found/
├── app.py              # Application factory, blueprint registration
├── config.py           # App configuration (DB URI, upload limits)
├── extensions.py       # Shared Flask extension instances
├── utils.py            # Secure file upload helper
├── seed.py             # DB init + default admin creation script
├── models/             # SQLAlchemy models (User, Admin, LostItem, FoundItem)
├── forms/               # Flask-WTF forms (auth + item forms)
├── routes/              # Blueprints: auth, main, items, admin
├── templates/            # Jinja2 templates (Bootstrap 5 UI)
├── static/               # CSS, JS, uploaded item images
└── database/             # SQLite database file lives here
```

## Modules
- **Authentication** — register, login, logout, hashed passwords, sessions
- **Student Dashboard** — stats, recent items, quick actions
- **Lost Item Reporting** — name, category, description, location, date, image
- **Found Item Reporting** — same fields, finder-side
- **Search** — filter by keyword, category, location, status, type
- **Item Details** — full info + contact number (visible to logged-in users)
- **Admin Panel** — separate login, view users/reports, delete fake reports,
  mark items returned, dashboard analytics

## Security Measures
- Passwords hashed with bcrypt (never stored in plain text)
- CSRF protection on every form (Flask-WTF)
- Server-side validation on all inputs (WTForms validators)
- Secure filename handling + extension whitelist + UUID renaming for uploads
- Upload size capped at 3 MB
- Separate Admin table/login so a compromised student account can't reach
  admin routes
- Custom 404 / 500 / 413 error handlers

## Future Scope
- AI-based matching between lost and found item descriptions
- Email/SMS notifications when a possible match is found
- QR-code verification for item pickup
- College ID card system integration
- Campus location map for lost/found hotspots
- Mobile app (Flutter/React Native) + push notifications
