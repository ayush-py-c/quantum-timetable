import os
import time
from urllib.parse import urlparse
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect
from contextlib import contextmanager

app = Flask(__name__)

# Get the connection URL from environment variable or fallback to default
url = os.getenv("DATABASE_URL", "mysql://root:MZCEtRFCHEgDmEOmQukoTZmRDqvCYEvZ@switchyard.proxy.rlwy.net:49211/railway")

# Parse the URL
parsed_url = urlparse(url)
username = parsed_url.username
password = parsed_url.password
host = parsed_url.hostname
port = parsed_url.port
database = parsed_url.path.lstrip('/')

def get_connection():
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        port=port,
        database=database
    )

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = get_connection()
        yield conn
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

@app.route('/')
def index():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM time_slot")
            slots = cursor.fetchall()

            cursor.execute("SELECT * FROM user_details")
            users = cursor.fetchall()

            cursor.execute("SELECT * FROM teacher_details")
            teachers = cursor.fetchall()

            cursor.execute("SELECT * FROM course_details")
            courses = cursor.fetchall()

        return render_template("index.html", slots=slots, users=users, teachers=teachers, courses=courses)
    except Exception as e:
        return f"Database error: {str(e)}", 500


@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        user_id = request.form['user_id']
        course_id = request.form['course_id']
        teacher_id = request.form['teacher_id']
        date_time = request.form['date_and_time']

        max_retries = 3
        retry_count = 0
        backoff_time = 1
        
        while retry_count < max_retries:
            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                conn.start_transaction()
                cursor.execute(
                    "INSERT INTO time_slot (user_id, course_id, teacher_id, date_and_time) VALUES (%s, %s, %s, %s)",
                    (user_id, course_id, teacher_id, date_time)
                )
                conn.commit()
                return redirect('/')
            except Error as e:
                if conn:
                    conn.rollback()
                if "lock wait timeout" in str(e).lower():
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(backoff_time * (2 ** (retry_count - 1)))
                        continue
                    else:
                        return "Database timeout after multiple retries. Please try again later.", 500
                else:
                    return f"Database error: {str(e)}", 500
            finally:
                if conn is not None and conn.is_connected():
                    conn.close()
    return render_template("add_entry.html")

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        data = (
            request.form['user_id'],
            request.form['user_name'],
            request.form['designation'],
            request.form['e_mail'],
            request.form['address']
        )
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO user_details (user_id, user_name, designation, e_mail, address) VALUES (%s, %s, %s, %s, %s)",
                    data
                )
                conn.commit()
                return redirect('/')
        except Exception as e:
            return f"Database error: {str(e)}", 500
    return render_template("add_user.html")

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        data = (
            request.form['teacher_id'],
            request.form['teacher_name'],
            request.form['qualifications'],
            request.form['phone_no']
        )
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO teacher_details (teacher_id, teacher_name, qualifications, phone_no) VALUES (%s, %s, %s, %s)",
                    data
                )
                conn.commit()
                return redirect('/')
        except Exception as e:
            return f"Database error: {str(e)}", 500
    return render_template("add_teacher.html")

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        data = (
            request.form['course_id'],
            request.form['course_name'],
            request.form['teacher_id'],
            request.form['room_no']
        )
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO course_details (course_id, course_name, teacher_id, room_no) VALUES (%s, %s, %s, %s)",
                    data
                )
                conn.commit()
                return redirect('/')
        except Exception as e:
            return f"Database error: {str(e)}", 500
    return render_template("add_course.html")

@app.errorhandler(500)
def handle_server_error(error):
    return "A database error occurred. Please try again or contact the administrator if the issue persists.", 500

if __name__ == '__main__':
    app.run(debug=True)
