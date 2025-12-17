from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="192.168.1.18",
    user="labplus",
    password="Labadmin123",
    database="demo_library"
)

@app.route("/")
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bookshelf")
    books = cursor.fetchall()
    return render_template("index.html", books=books)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    author = request.form["author"]
    category = request.form["category"]
    year = request.form["year"]

    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO bookshelf (title, author, category, published_year) VALUES (%s, %s, %s, %s)",
        (title, author, category, year)
    )
    db.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM bookshelf WHERE book_id = %s", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
