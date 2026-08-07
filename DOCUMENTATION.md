# Smart Lost & Found Portal for College Campus — Project Documentation

## 1. Problem Statement
Students frequently lose items such as ID cards, wallets, chargers,
earphones, laptops, keys, books, calculators, and water bottles inside
college campuses. There is no centralized platform where students can
report lost items, report found items, and reconnect with their belongings
— reports are currently scattered across WhatsApp groups and physical
notice boards, making recovery slow and unreliable.

## 2. Objectives
- Provide a single centralized platform to report and search lost/found items.
- Allow students to securely register, log in, and manage their own reports.
- Let students search reported items by name, category, location, date, or status.
- Give administrators tools to moderate reports and track recovery outcomes.
- Contribute to a cleaner, more trust-based, sustainable campus community.

## 3. Scope
The system covers student registration/login, lost and found item
reporting (with optional image upload), search/filtering, item detail
viewing with contact information, and an admin panel for moderation and
analytics. It does not cover payment processing, real-time chat, or
automated matching (listed under Future Scope).

## 4. Methodology
The application follows the MVC-like pattern natively supported by Flask:
- **Models** (SQLAlchemy) define the database schema.
- **Routes** (Flask Blueprints) handle request logic, split by concern
  (auth, main/dashboard, items, admin).
- **Templates** (Jinja2 + Bootstrap 5) render the UI, extending a shared
  base layout for consistent navigation and styling.
- **Forms** (Flask-WTF) provide both client- and server-side validation
  plus CSRF protection on every POST request.

Development proceeded in phases: schema design → auth → item reporting →
search → admin panel → styling/polish → testing.

## 5. Modules

| Module | Description |
|---|---|
| Authentication | Registration, login, logout, password hashing, session management |
| Student Dashboard | Stats (total lost/found, personal reports), recent items, quick actions |
| Lost Item Reporting | Form to report a lost item with image upload |
| Found Item Reporting | Form to report a found item with image upload |
| Search | Multi-filter search across both lost and found reports |
| Item Details | Full item view including reporter's contact number |
| Admin Panel | Separate login; view users/reports; delete fake reports; mark items returned; analytics dashboard |

## 6. Database Design

**users**: id, full_name, email (unique), phone, password_hash, created_at

**admins**: id, username (unique), password_hash

**lost_items**: id, item_name, category, description, location_lost,
date_lost, student_name, contact_number, image_filename, status
(Pending/Claimed/Returned), created_at, user_id (FK → users.id)

**found_items**: id, item_name, category, description, location_found,
date_found, finder_name, contact_number, image_filename, status
(Pending/Claimed/Returned), created_at, user_id (FK → users.id)

Relationships: one User → many LostItem, one User → many FoundItem
(cascade delete on user removal).

## 7. Technology Stack
- Backend: Python 3, Flask (application factory + Blueprints)
- Frontend: HTML5, CSS3, Bootstrap 5, vanilla JavaScript
- Database: SQLite
- ORM: SQLAlchemy (Flask-SQLAlchemy)
- Authentication: Flask-Login, Flask-Bcrypt
- Forms & Security: Flask-WTF (CSRF), WTForms validators

## 8. Testing
Manual end-to-end testing was performed covering:
- Student registration and login (including duplicate email and wrong
  password rejection)
- CSRF protection (requests missing a valid token are rejected)
- Reporting a lost item with all required fields
- Searching and filtering by keyword, confirming correct result counts
- Viewing item details, including contact-number gating for logged-out users
- Admin login, dashboard analytics, marking an item returned, and viewing
  users/reports lists
- 404 handling for invalid routes

All flows returned expected HTTP status codes and rendered correctly.

## 9. Results
A fully functional lost-and-found web portal was built and verified to run
without errors, supporting the complete lifecycle of a report: submission →
search/discovery → contact → resolution (marked returned by admin).

## 10. Future Scope
- AI-based matching between lost and found item descriptions
- Email and SMS notifications on possible matches
- QR-code verification for item pickup
- College ID card system integration
- Campus location map showing lost/found hotspots
- Mobile app (Flutter/React Native) with push notifications

## 11. Conclusion
The Smart Lost & Found Portal solves a real, everyday campus problem with a
lightweight, secure, and maintainable Flask application. It demonstrates
core full-stack skills — authentication, CRUD operations, file handling,
search/filtering, and role-based access control — while remaining scoped
appropriately for a B.Tech CSE mini project completed in 2 days.

## 12. References
- Flask documentation — https://flask.palletsprojects.com/
- Flask-SQLAlchemy documentation — https://flask-sqlalchemy.palletsprojects.com/
- Flask-Login documentation — https://flask-login.readthedocs.io/
- Bootstrap 5 documentation — https://getbootstrap.com/docs/5.3/
- UN Sustainable Development Goal 11 — https://sdgs.un.org/goals/goal11
