from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Management</title>
        <style>
            body {
                font-family: Arial;
                margin: 40px;
                background: #f4f4f4;
            }

            .container {
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
            }

            input, button {
                padding: 10px;
                margin: 5px;
            }

            button {
                background: #333;
                color: white;
                border: none;
                cursor: pointer;
            }

            table {
                width: 100%;
                margin-top: 20px;
                border-collapse: collapse;
            }

            th, td {
                padding: 10px;
                border: 1px solid #ddd;
            }
        </style>
    </head>

    <body>
        <div class="container">

        <h1>Student Management System</h1>

        <form action="/add" method="POST">
            <input type="text" name="name" placeholder="Student Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="text" name="course" placeholder="Course" required>
            <button type="submit">Add Student</button>
        </form>

        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Course</th>
                <th>Action</th>
            </tr>
    """

    for student in students:
        html += f"""
            <tr>
                <td>{student[0]}</td>
                <td>{student[1]}</td>
                <td>{student[2]}</td>
                <td>{student[3]}</td>
                <td>
                    <a href="/delete/{student[0]}">Delete</a>
                </td>
            </tr>
        """

    html += """
        </table>

        </div>
    </body>
    </html>
    """

    return html


@app.route("/add", methods=["POST"])
def add_student():

    name = request.form["name"]
    email = request.form["email"]
    course = request.form["course"]

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
        (name, email, course)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_student(id):

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)