import os
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# ----------------------------
# ฟังก์ชันเชื่อมต่อฐานข้อมูล
# ----------------------------
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

# ----------------------------
# หน้าแรก แสดงหนังสือ
# ----------------------------
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookshelf")
    books = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("index.html", books=books)

# ----------------------------
# เพิ่มหนังสือ
# ----------------------------
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    author = request.form["author"]
    category = request.form["category"]
    year = request.form["year"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO bookshelf (title, author, category, published_year)
        VALUES (%s, %s, %s, %s)
        """,
        (title, author, category, year)
    )
    db.commit()
    cursor.close()
    db.close()

    return redirect("/")

# ----------------------------
# ลบหนังสือ
# ----------------------------
@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM bookshelf WHERE book_id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()

    return redirect("/")
