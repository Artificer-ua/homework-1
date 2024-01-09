from pprint import pp

from sqlalchemy import and_, asc, desc, func, select

from db import session
from models import Grades, Group, Student, Subjects, Teachers


def select_1() -> list:
    """
    1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
    :return: list
    """
    result = (
        session.query(
            Student.fullname, func.round(func.avg(Grades.grade), 2).label("avg_grade")
        )
        .select_from(Grades)
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )
    return result


def select_2(subject: int) -> list:
    """
    2. Знайти студента із найвищим середнім балом з певного предмета.
    :return: list
    """
    result = (
        session.query(
            Student.fullname,
            Subjects.subjects,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Student)
        .join(Subjects)
        .filter(Subjects.id == subject)
        .group_by(Student.fullname, Subjects.subjects)
        .order_by(desc("avg_grade"))
        .limit(1)
        .all()
    )
    return result


def select_3(subject: int) -> list:
    """
    3. Знайти середній бал у групах з певного предмета.
    :return: list
    """
    result = (
        session.query(
            Subjects.subjects,
            Group.name,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Student)
        .join(Subjects)
        .join(Group)
        .filter(Subjects.id == subject)
        .group_by(Subjects.subjects, Group.name)
        .order_by(desc("avg_grade"))
        .all()
    )
    return result


def select_4() -> list:
    """
    4. Знайти середній бал на потоці (по всій таблиці оцінок).
    :return: list|dict
    """

    result = (
        session.query(func.round(func.avg(Grades.grade), 2)).select_from(Grades).all()
    )
    return result


def select_5(teacher: int) -> list:
    """
    5. Знайти які курси читає певний викладач.
    :return: list
    """
    result = (
        session.query(Teachers.fullname, Subjects.subjects)
        .select_from(Subjects)
        .join(Teachers)
        .filter(Teachers.id == teacher)
        .group_by(Teachers.fullname, Subjects.subjects)
        .order_by(Teachers.fullname)
        .all()
    )
    return result


def select_6(group: int) -> list:
    """
    5. Знайти список студентів у певній групі.
    :return: list
    """
    result = (
        session.query(Student.fullname, Group.name)
        .select_from(Student)
        .join(Group)
        .filter(Group.id == group)
        .group_by(Group.name, Student.fullname)
        .order_by(asc(Group.name))
        .all()
    )
    return result


def select_7(subject: int, group: int) -> list:
    """
    7. Знайти оцінки студентів у окремій групі з певного предмета.
    :return: list
    """

    result = (
        session.query(Student.fullname, Group.name, Grades.grade, Subjects.subjects)
        .select_from(Grades)
        .join(Student)
        .join(Subjects)
        .join(Group)
        .filter(and_(Subjects.id == subject, Group.id == group))
        .group_by(
            Student.fullname,
            Group.name,
            Grades.grade,
            Subjects.subjects,
        )
        .order_by(asc(Group.name))
        .all()
    )
    return result


def select_8(teacher: int) -> list:
    """
    8. Знайти середній бал, який ставить певний викладач зі своїх предметів.
    :return: list
    """

    result = (
        session.query(
            Teachers.fullname,
            Subjects.subjects,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Student)
        .join(Subjects)
        .join(Group)
        .join(Teachers)
        .filter(Subjects.teacher_id == teacher)
        .group_by(Subjects.subjects, Teachers.fullname)
        .order_by(asc(Subjects.subjects))
        .all()
    )
    return result


def select_9(student: int) -> list:
    """
    9. Знайти список курсів, які відвідує певний студент.
    :return: list
    """

    result = (
        session.query(Subjects.subjects, Student.fullname)
        .select_from(Grades)
        .join(Student)
        .join(Subjects)
        .join(Group)
        .filter(Student.id == student)
        .group_by(Student.fullname, Subjects.subjects)
        .order_by(asc(Subjects.subjects))
        .all()
    )
    return result


def select_10(student: int, teacher: int) -> list:
    """
    10. Список курсів, які певному студенту читає певний викладач.
    :return: list
    """

    result = (
        session.query(
            Teachers.fullname,
            Subjects.subjects,
            Student.fullname,
        )
        .select_from(Grades)
        .join(Student)
        .join(Subjects)
        .join(Group)
        .join(Teachers)
        .filter(and_(Student.id == student, Teachers.id == teacher))
        .group_by(Student.fullname, Teachers.fullname, Subjects.subjects)
        .order_by(asc(Subjects.subjects))
        .all()
    )
    return result


def select_add_1(student: int, teacher: int) -> list:
    """
    Додаткове 1. Середній бал, який певний викладач ставить певному студентові.
    :return: list
    """

    result = (
        session.query(
            Student.fullname,
            Teachers.fullname,
            func.round(func.avg(Grades.grade), 2).label("avg_grade"),
        )
        .select_from(Grades)
        .join(Student)
        .join(Subjects)
        .join(Teachers)
        .filter(and_(Student.id == student, Teachers.id == teacher))
        .group_by(Student.fullname, Teachers.fullname)
        .order_by("avg_grade")
        .all()
    )
    return result


def select_add_2(subject: int, group: int) -> list:
    """
    Додаткове 2. Оцінки студентів у певній групі з певного предмета на останньому занятті.
    :return: list
    """
    subquery = (
        select(func.max(Grades.update_at).label("last"))
        .join(Student)
        .join(Group)
        .filter(and_(Group.id == group, Grades.subject_id == subject))
        .order_by(desc("last"))
        .limit(1)
        .scalar_subquery()
    )

    result = (
        session.query(
            Student.fullname,
            Subjects.subjects,
            Group.name,
            Grades.update_at,
            Grades.grade,
        )
        .select_from(Grades)
        .join(Student)
        .join(Subjects)
        .join(Group)
        .filter(
            and_(
                Subjects.id == subject, Group.id == group, Grades.update_at == subquery
            )
        )
        .group_by(
            Student.fullname,
            Subjects.subjects,
            Group.name,
            Grades.update_at,
            Grades.grade,
        )
        .order_by(desc(Grades.update_at))
        .all()
    )
    return result


if __name__ == "__main__":
    pp(("Select 1: ", select_1()))
    pp(("Select 2: ", select_2(1)))
    pp(("Select 3: ", select_3(2)))
    pp(("Select 4: ", select_4()))
    pp(("Select 5: ", select_5(2)))
    pp(("Select 6: ", select_6(3)))
    pp(("Select 7: ", select_7(4, 1)))
    pp(("Select 8: ", select_8(3)))
    pp(("Select 9: ", select_9(10)))
    pp(("Select 10: ", select_10(4, 2)))

    pp(("Additional select 1: ", select_add_1(50, 2)))
    pp(("Additional select 2: ", select_add_2(2, 2)))
