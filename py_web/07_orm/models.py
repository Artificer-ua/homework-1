from sqlalchemy import Column, Date, ForeignKey, Integer, String,  func  # , event
from sqlalchemy.orm import relationship

from db import Base

# from sqlalchemy.ext.hybrid import hybrid_property


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(8), nullable=False)


# class Person():
#     first_name = Column(String(20))
#     last_name = Column(String(20), nullable=False)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, autoincrement=True, primary_key=True)
    fullname = Column(String(50), nullable=False)
    group_id = Column(
        Integer, ForeignKey("groups.id"), onupdate="CASCADE", nullable=True
    )  # ondelete="SET NULL")
    group = relationship("Group", backref="students")

    # @hybrid_property
    # def full_name(self):
    #     return self.last_name + " " + self.first_name


class Teachers(Base):
    __tablename__ = "teachers"
    id = Column(Integer, autoincrement=True, primary_key=True)
    fullname = Column(String(50), nullable=False)


class Subjects(Base):
    __tablename__ = "subjects"
    id = Column(Integer, autoincrement=True, primary_key=True)
    subjects = Column(String(20), nullable=False)
    teacher_id = Column(
        Integer, ForeignKey("teachers.id"), onupdate="CASCADE", nullable=True
    )  # ondelete="SET NULL")
    teacher = relationship("Teachers", backref="subjects")


class Grades(Base):
    __tablename__ = "grades"
    id = Column(Integer, autoincrement=True, primary_key=True)
    grade = Column(Integer, nullable=True)
    student_id = Column(
        Integer, ForeignKey("students.id"), onupdate="CASCADE", nullable=True
    )  # , ondelete="SET NULL")
    subject_id = Column(
        Integer, ForeignKey("subjects.id"), onupdate="CASCADE", nullable=True
    )  # , ondelete="SET NULL")
    update_at = Column(Date, default=func.now)
    stud = relationship("Student", backref="grades")
    subj = relationship("Subjects", backref="grades")


# @event.listens_for(Grades, "before_update")
# def update_update_at(mapper, connection, target):
#     target.update_at = func.now
