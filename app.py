from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
db = None
cursor = None

try:
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root123",
        database="grocery_db",
        auth_plugin="mysql_native_password"
    )
    cursor = db.cursor()
    print("Database connected")
except:
    print("Database not connected (cloud environment)")


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # ✅ Prevent 500 error on Render
        if cursor is None:
            return "Database not available in cloud. Please run locally.", 503

        username = request.form.get("username")
        password = request.form.get("password")

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- ADD PRODUCT ----------------
@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    # ✅ Prevent DB crash on cloud
    if cursor is None:
        return "Database not available in cloud. Please run locally.", 503

    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        quantity = request.form.get("quantity")

        cursor.execute(
            "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)",
            (name, price, quantity)
        )
        db.commit()
        return redirect(url_for("view_products"))

    return render_template("add_product.html")


# ---------------- VIEW PRODUCTS ----------------
@app.route("/view_products")
def view_products():

    # ✅ Prevent DB crash on cloud
    if cursor is None:
        return "Database not available in cloud. Please run locally.", 503

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return render_template("view_products.html", products=products)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
