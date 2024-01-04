POSTGRES_HOST = "10.10.5.13"
POSTGRES_PORT = "5432"
POSTGRES_DATABASE = "pyweb"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "pass"

GROUPS = ["KI-32", "KN-11", "IS-23"]
SUBJECTS = ["MATH", "UKRAINIAN", "HISTORY", "ENGLISH", "PHILOSOPHY", "PROGRAMMING"]
TEACHERS_COUNT = 5
STUDENTS_COUNT = 50
GRADES_COUNT = 20

SCRIPTS_DIR = "sql_scripts"

TABLE_NAMES = ["classes", "students", "teachers", "subjects", "grades"]

SQL_INSERT_GROUPS_TABLE = "INSERT INTO classes(clas) VALUES(%s)"
SQL_INSERT_STUDENTS_TABLE = "INSERT INTO students(fullname, class_id) VALUES(%s, %s)"
SQL_INSERT_TEACHERS_TABLE = "INSERT INTO teachers(fullname) VALUES(%s)"
SQL_INSERT_SUBJECTS_TABLE = "INSERT INTO subjects(subjects, teacher_id) VALUES(%s, %s)"
SQL_INSERT_GRADES_TABLE = "INSERT INTO grades(grade, student_id, subject_id, created_at) VALUES(%s, %s, %s, %s)"

TABLE_GROUPS = """CREATE TABLE IF NOT EXISTS classes (
    id SMALLSERIAL PRIMARY KEY,
    clas VARCHAR(8) UNIQUE
);"""

TABLE_STUDENTS = """CREATE TABLE IF NOT EXISTS students (
  id SMALLSERIAL PRIMARY KEY,
  fullname VARCHAR(30),
  class_id INT,
  FOREIGN KEY (class_id) REFERENCES classes (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);"""

TABLE_TEACHERS = """CREATE TABLE IF NOT EXISTS teachers (
  id SMALLSERIAL PRIMARY KEY,
  fullname VARCHAR(20)
);"""

TABLE_SUBJECTS = """CREATE TABLE IF NOT EXISTS subjects (
  id SMALLSERIAL PRIMARY KEY,
  subjects VARCHAR(20),
  teacher_id SMALLINT,
  FOREIGN KEY (teacher_id) REFERENCES teachers (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);"""

TABLE_GRADES = """CREATE TABLE IF NOT EXISTS grades (
  id SMALLSERIAL PRIMARY KEY,
  grade INT CHECK (grade > 0 AND grade <= 5),
  student_id SMALLINT,
  subject_id SMALLINT,
  created_at DATE,
  FOREIGN KEY (student_id) REFERENCES students (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
  FOREIGN KEY (subject_id) REFERENCES subjects (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);"""

SQL_TABLES = [
    TABLE_GROUPS,
    TABLE_STUDENTS,
    TABLE_TEACHERS,
    TABLE_SUBJECTS,
    TABLE_GRADES,
]
