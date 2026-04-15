# Flask Project - Google Auth Demo

A Flask web application that supports user registration, login, Google Authenticator OTP verification, username recovery, and password reset.

## Project Structure

- `app.py` - main Flask application and route definitions
- `templates/` - HTML page templates
  - `home.html`
  - `login.html`
  - `signup.html`
  - `NewHome.html`
  - `showqr.html`
  - `verify_otp.html`
  - `forgotusername.html`
  - `forgotpassword.html`
- `static/` - stylesheets and generated QR images
  - `forgot.css`
  - `home.css`
  - `login.css`
  - `newhomepage.css`
  - `signup.css`
  - `verify_opt.css`
  - `qr_*.png` - generated QR code images for each user
- `venv/` - Python virtual environment (not required if using a separate env)
- `package.json` - Node dependency metadata (contains `mysql2` but is not used by the Flask app)

## Features

- Home page
- User signup
- Login with username/password
- Google Authenticator OTP verification after login
- QR code generation for 2FA setup
- Forgot username by email lookup
- Forgot password reset

## Required Python Packages

Install the required packages before running the app:

```powershell
.\venv\Scripts\Activate.ps1
pip install Flask mysql-connector-python pyotp qrcode pillow
```

If not using the included virtual environment, run:

```powershell
python -m pip install Flask mysql-connector-python pyotp qrcode pillow
```

## Database Setup

The app connects to a MySQL database with these credentials (hard-coded in `app.py`):

- host: `localhost`
- user: `root`
- password: `Shyam@123`
- database: `Shyam`

Create the database and table using SQL:

```sql
CREATE DATABASE Shyam;
USE Shyam;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(255),
  username VARCHAR(255) UNIQUE,
  password VARCHAR(255),
  emailid VARCHAR(255),
  SECERET_KEY VARCHAR(255)
);
```

## Running the App

From the project root:

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## Important Notes

- The database connection parameters are hard-coded in `app.py`. Update them if your MySQL credentials differ.
- The app stores user passwords in plain text. For production, use password hashing instead.
- The app generates QR codes in `static/` using the TOTP provisioning URI.
- `package.json` currently lists only `mysql2`, which is not required for the Python Flask app.

## Routes

- `/` - home
- `/login` - login page
- `/signup` - signup page
- `/logout` - returns home page
- `/loginsubmit` - login form submit
- `/createuser` - signup form submit
- `/showqr/<username>` - display QR code for 2FA setup
- `/verify-otp` - OTP verification
- `/forgotusername` - forgot username page
- `/forgot-password` - forgot password page
- `/forgot-username` - username recovery form submit
- `/forgot-password` - password reset form submit

## Improvements

Possible improvements for this project:

- Add password hashing with `werkzeug.security`
- Replace hard-coded DB credentials with environment variables
- Add input validation and flash messages
- Remove unused Node dependencies or add a proper frontend workflow
- Clean up generated QR code files after use
