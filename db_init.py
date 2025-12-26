import os
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
from dotenv import load_dotenv
import psycopg

# Load environment variables from .env if present
load_dotenv()

# Read Neon/Postgres connection URL from env
# Examples:
#   postgresql://user:password@host/dbname?sslmode=require
#   postgres://user:password@host/dbname?sslmode=require
url = os.getenv("DATABASE_URL") or os.getenv("NEON_DATABASE_URL")
if not url:
    raise RuntimeError(
        "DATABASE_URL (or NEON_DATABASE_URL) not set. Provide your Neon connection string."
    )

# Ensure sslmode=require for Neon
parsed_url = urlparse(url)
query = parse_qs(parsed_url.query)
if "sslmode" not in query:
    query["sslmode"] = ["require"]
new_query = urlencode({k: v[0] for k, v in query.items()})
url_with_ssl = urlunparse(
    (
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment,
    )
)

# Connect to Neon/Postgres
connection = psycopg.connect(url_with_ssl)
cursor = connection.cursor()

try:
    # Extract database name for logging
    database = parsed_url.path.lstrip("/") or "public"
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
            date_and_time TIMESTAMP,
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
        ON CONFLICT (user_id) DO UPDATE SET
            user_name = EXCLUDED.user_name,
            designation = EXCLUDED.designation,
            e_mail = EXCLUDED.e_mail,
            address = EXCLUDED.address;
    """)

    cursor.execute("""
        INSERT INTO teacher_details (teacher_id, teacher_name, qualifications, phone_no)
        VALUES 
        ('t1', 'Dr. Sharma', 'PhD Mathematics', 9876),
        ('t2', 'Prof. Roy', 'M.Tech Physics', 91234)
        ON CONFLICT (teacher_id) DO UPDATE SET
            teacher_name = EXCLUDED.teacher_name,
            qualifications = EXCLUDED.qualifications,
            phone_no = EXCLUDED.phone_no;
    """)

    cursor.execute("""
        INSERT INTO course_details (course_id, course_name, teacher_id, room_no)
        VALUES 
        ('c1', 'Discrete Math', 't1', 101),
        ('c2', 'Quantum Physics', 't2', 102)
        ON CONFLICT (course_id) DO UPDATE SET
            course_name = EXCLUDED.course_name,
            teacher_id = EXCLUDED.teacher_id,
            room_no = EXCLUDED.room_no;
    """)

    cursor.execute("""
        INSERT INTO time_slot (user_id, course_id, teacher_id, date_and_time)
        VALUES 
        ('u1', 'c1', 't1', '2025-04-28 10:00:00'),
        ('u2', 'c2', 't2', '2025-04-28 12:00:00');
    """)

    connection.commit()
    print("✅ Tables created and sample data inserted.")

    # Step 3: Show tables in public schema (Postgres)
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    print(f"Tables in {database} database:")
    for (table_name,) in cursor.fetchall():
        print(f"- {table_name}")

except psycopg.Error as error:
    print(f"❌ Error: {error}")
    connection.rollback()

finally:
    cursor.close()
    connection.close()
    print("🔒 Connection closed.")
