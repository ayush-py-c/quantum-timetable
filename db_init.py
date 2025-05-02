import mysql.connector
from urllib.parse import urlparse

# Parse the connection URL
url = "mysql://root:bbkrrOQWsbwkZOCPPwbamagIiGfIOvKd@mainline.proxy.rlwy.net:50114/railway"
parsed_url = urlparse(url)

# Extract connection parameters
username = parsed_url.username
password = parsed_url.password
host = parsed_url.hostname
port = parsed_url.port
database = parsed_url.path.lstrip('/')  # 'railway'

# Connect directly to the Railway database
connection = mysql.connector.connect(
    user=username,
    password=password,
    host=host,
    port=port,
    database=database
)
cursor = connection.cursor()

try:
    print(f"Using database: {database}")

    # Step 1: Create tables
    tables = {
        "user_details": """
        CREATE TABLE IF NOT EXISTS user_details (
            user_id VARCHAR(20) PRIMARY KEY,
            user_name VARCHAR(100),
            designation VARCHAR(50),
            e_mail VARCHAR(100),
            address VARCHAR(200)
        );
        """,
        "teacher_details": """
        CREATE TABLE IF NOT EXISTS teacher_details (
            teacher_id VARCHAR(20) PRIMARY KEY,
            teacher_name VARCHAR(100),
            qualifications VARCHAR(100),
            phone_no BIGINT
        );
        """,
        "course_details": """
        CREATE TABLE IF NOT EXISTS course_details (
            course_id VARCHAR(20) PRIMARY KEY,
            course_name VARCHAR(100),
            teacher_id VARCHAR(20),
            room_no INT,
            FOREIGN KEY (teacher_id) REFERENCES teacher_details(teacher_id)
        );
        """,
        "time_slot": """
        CREATE TABLE IF NOT EXISTS time_slot (
            user_id VARCHAR(20),
            course_id VARCHAR(20),
            teacher_id VARCHAR(20),
            date_and_time DATETIME,
            FOREIGN KEY (user_id) REFERENCES user_details(user_id),
            FOREIGN KEY (course_id) REFERENCES course_details(course_id),
            FOREIGN KEY (teacher_id) REFERENCES teacher_details(teacher_id)
        );
        """
    }

    for table_name, query in tables.items():
        print(f"Creating table {table_name}...")
        cursor.execute(query)

    # Step 2: Insert sample data
    print("Inserting sample data...")

    cursor.execute("""
        INSERT INTO user_details (user_id, user_name, designation, e_mail, address)
        VALUES 
        ('u1', 'Aryan', 'Professor', 'aryan@example.com', 'Bangalore'),
        ('u2', 'Neha', 'Assistant Professor', 'neha@example.com', 'Delhi')
        ON DUPLICATE KEY UPDATE user_name=VALUES(user_name);
    """)

    cursor.execute("""
        INSERT INTO teacher_details (teacher_id, teacher_name, qualifications, phone_no)
        VALUES 
        ('t1', 'Dr. Sharma', 'PhD Mathematics', 9876),
        ('t2', 'Prof. Roy', 'M.Tech Physics', 91234)
        ON DUPLICATE KEY UPDATE teacher_name=VALUES(teacher_name);
    """)

    cursor.execute("""
        INSERT INTO course_details (course_id, course_name, teacher_id, room_no)
        VALUES 
        ('c1', 'Discrete Math', 't1', 101),
        ('c2', 'Quantum Physics', 't2', 102)
        ON DUPLICATE KEY UPDATE course_name=VALUES(course_name);
    """)

    cursor.execute("""
        INSERT INTO time_slot (user_id, course_id, teacher_id, date_and_time)
        VALUES 
        ('u1', 'c1', 't1', '2025-04-28 10:00:00'),
        ('u2', 'c2', 't2', '2025-04-28 12:00:00');
    """)

    connection.commit()
    print("✅ Tables created and sample data inserted.")

    # Step 3: Show tables
    cursor.execute("SHOW TABLES;")
    print(f"Tables in {database} database:")
    for table in cursor.fetchall():
        print(f"- {table[0]}")

except mysql.connector.Error as error:
    print(f"❌ Error: {error}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()
    print("🔒 Connection closed.")
