import os
import time
from urllib.parse import urlparse
import mysql.connector
from mysql.connector import Error
from flask import Flask, render_template, request, redirect
from contextlib import contextmanager

app = Flask(__name__)

# Get the connection URL from environment variable or fallback to default
url = os.getenv("DATABASE_URL", "mysql://root:YHwYuhkYhEKsOuxhDQVcMhemgTMdDbKU@switchback.proxy.rlwy.net:59007/railway")

# Parse the URL
parsed_url = urlparse(url)

# Extract connection parameters
username = parsed_url.username
password = parsed_url.password
host = parsed_url.hostname
port = parsed_url.port
database = parsed_url.path.lstrip('/')

# Basic connection function
def get_connection():
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        port=port,
        database=database
    )

# Context manager for safer connection handling
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
        return render_template("index.html", slots=slots)
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
        backoff_time = 1  # Start with 1 second backoff
        
        while retry_count < max_retries:
            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                
                # Start transaction explicitly
                conn.start_transaction()
                
                cursor.execute(
                    "INSERT INTO time_slot (user_id, course_id, teacher_id, date_and_time) VALUES (%s, %s, %s, %s)",
                    (user_id, course_id, teacher_id, date_time)
                )
                
                conn.commit()
                return redirect('/')
                
            except Error as e:
                if conn:
                    conn.rollback()  # Roll back the transaction if there's an error
                
                if "lock wait timeout" in str(e).lower():
                    retry_count += 1
                    if retry_count < max_retries:
                        # Exponential backoff
                        sleep_time = backoff_time * (2 ** (retry_count - 1))
                        time.sleep(sleep_time)
                        continue
                    else:
                        return "Database timeout after multiple retries. Please try again later.", 500
                else:
                    # If it's another kind of error, report it
                    return f"Database error: {str(e)}", 500
            finally:
                if conn is not None and conn.is_connected():
                    conn.close()
                    
    return render_template("add_entry.html")

# Add a simple error handler for database-related errors
@app.errorhandler(500)
def handle_server_error(error):
    return "A database error occurred. Please try again or contact the administrator if the issue persists.", 500

if __name__ == '__main__':
    app.run(debug=True)