CREATE DATABASE timetable_management;
USE timetable_management;

CREATE TABLE user_details (
  user_id VARCHAR(20) PRIMARY KEY,
  user_name VARCHAR(100),
  designation VARCHAR(50),
  e_mail VARCHAR(100),
  address VARCHAR(200)
);

CREATE TABLE teacher_details (
  teacher_id VARCHAR(20) PRIMARY KEY,
  teacher_name VARCHAR(100),
  qualifications VARCHAR(100),
  phone_no INT
);

CREATE TABLE course_details (
  course_id VARCHAR(20) PRIMARY KEY,
  course_name VARCHAR(100),
  teacher_id VARCHAR(20),
  room_no INT,
  FOREIGN KEY (teacher_id) REFERENCES teacher_details(teacher_id)
);

CREATE TABLE time_slot (
  user_id VARCHAR(20),
  course_id VARCHAR(20),
  teacher_id VARCHAR(20),
  date_and_time DATETIME,
  FOREIGN KEY (user_id) REFERENCES user_details(user_id),
  FOREIGN KEY (course_id) REFERENCES course_details(course_id),
  FOREIGN KEY (teacher_id) REFERENCES teacher_details(teacher_id)
);


-- INSERT into user_details ("a1", "Aryan ", "banglore", "teacher@123", "unknown");
-- INSERT into teacher_details ("t1", "Aryan ", "B.tech", 123456789);
-- INSERT INTO TEACHER_DETAILS("t2","Ayush","Banglore","ayu@gmail.com","unknown");
-- INSERT into course_details ("a1","maths","t1","20");

COMMIT;
