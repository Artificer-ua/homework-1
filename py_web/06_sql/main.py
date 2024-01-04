import os
from datetime import datetime, timedelta
from pprint import pp
from random import choice, randint

from faker import Faker
from psycopg2 import DatabaseError

from connection import create_connection
from headers import (GRADES_COUNT, GROUPS, SCRIPTS_DIR,
                     SQL_INSERT_GRADES_TABLE, SQL_INSERT_GROUPS_TABLE,
                     SQL_INSERT_STUDENTS_TABLE, SQL_INSERT_SUBJECTS_TABLE,
                     SQL_INSERT_TEACHERS_TABLE, SQL_TABLES, STUDENTS_COUNT,
                     SUBJECTS, TABLE_NAMES, TEACHERS_COUNT)

fake = Faker(locale="uk_UA")

sql_files_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), SCRIPTS_DIR)


def table_operation(conn, table_sql: str) -> None:
    try:
        c = conn.cursor()
        c.execute(table_sql)
    except DatabaseError as err:
        print(err)


def create_database_tables(tables: list):
    # create tables from list of tables
    with create_connection() as conn:
        for table in tables:
            if conn is not None:
                table_operation(conn, table)
            else:
                print("Error: can't create the database connection")


def del_all_tables(tables: list):
    with create_connection() as conn:
        for table in tables:
            if conn is not None:
                table_operation(conn, f"DROP TABLE IF EXISTS {table} CASCADE;")
            else:
                print("Error: can't create the database connection")


def clear_all_tables(tables: list):
    with create_connection() as conn:
        for table in tables:
            if conn is not None:
                table_operation(conn, f"TRUNCATE TABLE {table};")
            else:
                print("Error: can't create the database connection")


def fill_table(sql_insert: str, sql_values: tuple):
    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()
            cur.execute(sql_insert, sql_values)
            cur.close()
        else:
            print("Error: can't create the database connection")


def fill_many(sql_insert: str, sql_values: list):
    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()
            cur.executemany(sql_insert, sql_values)
            cur.close()
        else:
            print("Error: can't create the database connection")


# def perform_query(query_str):
#     with create_connection() as conn:
#         if conn is not None:
#             cur = conn.cursor()
#             cur.execute(query_str)
#             pp(cur.fetchall())
#             # result = cur.fetchall()
#             cur.close()
#         else:
#             print("Error: can't create the database connection")
#     # return result


def perform_query_script(script: str) -> list:
    with create_connection() as conn:
        if conn is not None:
            cur = conn.cursor()
            cur.execute(open(os.path.join(sql_files_folder, script), "r").read())
            result = cur.fetchall()
            cur.close()
        else:
            print("Error: can't create the database connection")
    return result


def create_all_data():
    # delete all tables for tests
    del_all_tables(TABLE_NAMES)

    # creating tables from predefined list
    create_database_tables(SQL_TABLES)

    # filling group table
    for i, group in enumerate(GROUPS):
        fill_table(SQL_INSERT_GROUPS_TABLE, (group,))

    # filling teachers table
    for i in range(0, TEACHERS_COUNT):
        fill_table(SQL_INSERT_TEACHERS_TABLE, (fake.name(),))

    # filling subjects table (Sometimes, there are extreamly talanted techers..or teachers with time managment problems)
    for subject in SUBJECTS:
        fill_table(SQL_INSERT_SUBJECTS_TABLE, (subject, randint(1, TEACHERS_COUNT)))

    # filling students table (Not very fair distribution by groups)
    for _ in range(0, STUDENTS_COUNT):
        fill_table(
            SQL_INSERT_STUDENTS_TABLE, (fake.name(), choice(range(1, len(GROUPS) + 1)))
        )

    # filling grades (Most of students are not so clever.. may be because of extreamly talanted techers)
    start_date = datetime.strptime("01.09.2022", "%d.%m.%Y")
    end_date = datetime.strptime("20.06.2023", "%d.%m.%Y")
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.isoweekday() < 6:
            dates.append(current_date)
        current_date += timedelta(days=1)

    grades = []
    for day in dates:
        subj = randint(1, len(SUBJECTS))
        stud = [randint(1, STUDENTS_COUNT) for _ in range(7)]
        for student in stud:
            grades.append((randint(2, 5), student, subj, day.date()))

    fill_many(SQL_INSERT_GRADES_TABLE, grades)


if __name__ == "__main__":
    # Use to create new tables and fill it with some fake data
    create_all_data()

    # only for testing, without formatting.
    print(
        "SQL request #1: Знайти 5 студентів із найбільшим середнім балом з усіх предметів."
    )
    pp(perform_query_script("query_1.sql"))

    print(
        "\nSQL request #2: Знайти студента із найвищим середнім балом з певного предмета."
    )
    pp(perform_query_script("query_2.sql"))

    print("\nSQL request #3: Знайти середній бал у групах з певного предмета.")
    pp(perform_query_script("query_3.sql"))

    print("\nSQL request #4: Знайти середній бал на потоці (по всій таблиці оцінок).")
    pp(perform_query_script("query_4.sql"))

    print("\nSQL request #5: Знайти які курси читає певний викладач.")
    pp(perform_query_script("query_5.sql"))

    print("\nSQL request #6: Знайти список студентів у певній групі.")
    pp(perform_query_script("query_6.sql"))

    print(
        "\nSQL request #7: Знайти оцінки студентів у окремій групі з певного предмета."
    )
    pp(perform_query_script("query_7.sql"))

    print(
        "\nSQL request #8: Знайти середній бал, який ставить певний викладач зі своїх предметів."
    )
    pp(perform_query_script("query_8.sql"))

    print("\nSQL request #9: Знайти список курсів, які відвідує студент.")
    pp(perform_query_script("query_9.sql"))

    print(
        "\nSQL request #10: Список курсів, які певному студенту читає певний викладач."
    )
    some_result = perform_query_script("query_10.sql")
    for element in some_result:
        print(f"Teacher: {element[0]} - Course: {element[1]} - Student: {element[2]}")
