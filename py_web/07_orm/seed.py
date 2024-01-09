from datetime import datetime, timedelta
from random import choice, randint

from faker import Faker

from db import session
from headers import GRADES_COUNT, GROUPS, STUDENTS_COUNT, SUBJECTS, TEACHERS_COUNT
from models import Grades, Group, Student, Subjects, Teachers

fake = Faker(locale="uk_UA")


# Naming of variables and fields is terrible, but used from previous homework


# insert groups names from predefined list
def create_groups() -> None:
    for grp in GROUPS:
        group = Group(name=grp)
        session.add(group)
    # session.commit()


# filling students table (Not very fair distribution by groups.. as in the previous example)
def create_students() -> None:
    for _ in range(0, STUDENTS_COUNT):
        student = Student(
            fullname=fake.name(), group_id=choice(range(1, len(GROUPS) + 1))
        )
        session.add(student)
    # session.commit()


def create_teachers() -> None:
    for _ in range(0, TEACHERS_COUNT):
        teacher = Teachers(fullname=fake.name())
        session.add(teacher)
    # session.commit()


# filling subjects table (Sometimes, there are extreamly talanted techers..or teachers with time managment problems)
# as in the previous example
def create_subjects() -> None:
    for sbj in SUBJECTS:
        subject = Subjects(subjects=sbj, teacher_id=randint(1, TEACHERS_COUNT))
        session.add(subject)
    # session.commit()


# filling grades (Most of students are not so clever.. may be because of extreamly talanted techers)
def create_grades() -> None:
    start_date = datetime.strptime("01.09.2022", "%d.%m.%Y")
    end_date = datetime.strptime("20.06.2023", "%d.%m.%Y")
    dates = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.isoweekday() < 6:
            dates.append(current_date)
        current_date += timedelta(days=1)

    for day in dates:
        for _ in range(7):
            gradee = Grades(
                grade=randint(2, 5),
                student_id=randint(1, STUDENTS_COUNT),
                subject_id=randint(1, len(SUBJECTS)),
                update_at=day.date(),
            )
            session.add(gradee)
    # session.commit()


if __name__ == "__main__":
    # start filling tables
    create_groups()
    create_students()
    create_teachers()
    create_subjects()
    create_grades()

    # commit all
    session.commit()
