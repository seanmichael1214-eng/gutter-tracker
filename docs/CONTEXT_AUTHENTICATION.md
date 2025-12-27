Authentication Context
======================

Overview
- The app uses a simple password check against APP_PASSWORD loaded from environment configuration. A user submits the password via the login form; if it matches, a session flag is set and the user can access protected routes.

How APP_PASSWORD is sourced
- Config loaded from app.config.Config via Flask app factory.
- APP_PASSWORD = os.getenv("APP_PASSWORD", "changeme").
- In development, a .env file (read via python-dotenv) typically defines APP_PASSWORD; in production environments, set APP_PASSWORD in the hosting environment.

Login flow (high level)
- GET /login shows the login form.
- POST /login compares the provided password (trimmed) to APP_PASSWORD.
- On success, session["logged_in"] = True and user is redirected to /dashboard.
- On failure, an error is shown and login is retried.

Current security posture
- Passwords are compared in plain text (not hashed).
- Sessions rely on Flask's SECRET_KEY and cookies.
- No CSRF protection is shown on the login form in the template.

Common failure modes
- APP_PASSWORD not set in environment (uses default "changeme").
- Hidden environment variables not loaded in production (e.g., .env not present).
- Whitespace or trailing spaces in the password value (addressed by trimming input).
- Browser cookies cleared or sessions expired (clears login).

Recommended improvements (next steps)
- Replace plaintext password check with hashed password (bcrypt/argon2) and store a user record in a DB.
- Introduce Flask-Login for robust session management.
- Add CSRF protection to the login form.
- Provide a password reset mechanism or admin override for recovery.
- Document the authentication flow and troubleshooting steps in this page and TROUBLESHOOTING.md.

Quick reference (quick checks)
- APP_PASSWORD in config: os.getenv("APP_PASSWORD", "changeme").
- If login fails, check server logs for login attempts and remote IP address.

Assumptions
- The current project is primarily a lightweight internal tool; security hardening is planned but not yet completed.
- The environment providing APP_PASSWORD is trusted for development and staging; production should enforce stronger controls.
