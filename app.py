from flask import Flask, redirect, render_template, request, url_for
import mysql.connector
import pyotp
import qrcode

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
def get_db_connnection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shyam@123",
        database="Shyam"
    )

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('home.html')

# ---------------- AUTH PAGES ----------------
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    return render_template('home.html')

@app.route("/forgotusername")
def forgotusername():
    return render_template("forgotusername.html")

@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgotpassword.html")

# ---------------- LOGIN SUBMIT ----------------
@app.route("/loginsubmit", methods=["GET", "POST"])
def loginsubmit():
    msg = ""
    if request.method == "POST":
        usernm = request.form["username"]
        passwd = request.form["password"]

        conn = get_db_connnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s", (usernm,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and passwd == user["password"]:
            # Password OK → go to OTP
            return redirect(url_for("verify_otp_logic", username=usernm))
        else:
            msg = "Incorrect Username or Password!"

    return render_template("login.html", msg=msg)

# ---------------- CREATE ACCOUNT ----------------
@app.route("/createuser", methods=["GET", "POST"])
def CreateAccount():
    msg = ""
    if request.method == "POST":
        fullname = request.form["name"]
        usernm = request.form["username"]
        emailID = request.form["email"]
        passwd = request.form["password"]
        confirmPasswd = request.form["confirm_password"]

        if passwd != confirmPasswd:
            msg = "Passwords do not match!"
            return render_template("signup.html", msg=msg)

        secretkey = pyotp.random_base32()

        conn = get_db_connnection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (Name, username, password, emailid, SECERET_KEY) VALUES (%s,%s,%s,%s,%s)",
            (fullname, usernm, passwd, emailID, secretkey)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("showqr", username=usernm))

    return render_template("signup.html", msg=msg)

# ---------------- QR CODE ----------------
@app.route("/showqr/<username>")
def showqr(username):
    conn = get_db_connnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT SECERET_KEY FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    ga_key = user["SECERET_KEY"]
    totp = pyotp.TOTP(ga_key)
    otp_url = totp.provisioning_uri(name=username, issuer_name="Flask Project")

    img = qrcode.make(otp_url)
    qr_path = f"static/qr_{username}.png"
    img.save(qr_path)

    return render_template("showqr.html", qr_image=qr_path, secret=ga_key)

# ---------------- VERIFY OTP ----------------
@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp_logic():
    msg = ""
    username = request.args.get("username") or request.form.get("username")

    if request.method == "POST":
        otp_code = request.form["otp"]
        username = request.form["username"]

        conn = get_db_connnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT SECERET_KEY FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            totp = pyotp.TOTP(user["SECERET_KEY"])
            if totp.verify(otp_code):
                return render_template("NewHome.html", username=username)
            else:
                msg = "Invalid OTP. Please try again."
        else:
            msg = "User not found."

    return render_template("verify_otp.html", username=username, msg=msg)

# ---------------- FORGOT USERNAME ----------------
@app.route("/forgot-username", methods=["GET", "POST"])
def forgot_username():
    msg = ""
    found_username = None

    if request.method == "POST":
        email = request.form["email"]

        conn = get_db_connnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username FROM users WHERE emailid=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            found_username = user["username"]
        else:
            msg = "No account found with that email."

    return render_template("forgotusername.html", msg=msg, username=found_username)

# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    msg = ""
    success = False

    if request.method == "POST":
        username = request.form["username"]
        new_password = request.form["new_password"]

        conn = get_db_connnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if not user:
            msg = "No user found with that username."
        else:
            cursor.execute(
                "UPDATE users SET password=%s WHERE username=%s",
                (new_password, username)
            )
            conn.commit()
            success = True
            msg = "Password updated successfully!"

        cursor.close()
        conn.close()

    return render_template("forgotpassword.html", msg=msg, success=success)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
