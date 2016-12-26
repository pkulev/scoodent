
from collections import namedtuple
"""Kisqpy models."""

from sqlalchemy import (
    Column, Date, Enum, ForeignKey, Integer, String, Text, Boolean
)
from sqlalchemy.orm import relationship

from scoodent.common.db import Base


_TReportType = namedtuple("TReportEnumType", [
    "exam", "coursework", "credit"
])
"""Represents TReport enum type."""

TReportEnum = _TReportType("exam", "coursework", "credit")
"""TReport mapping."""

TReport = Enum(
    TReportEnum.exam,
    TReportEnum.coursework,
    TReportEnum.credit,
    name="treport")


class Student(Base):
    """Student DAO representation."""

    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    surname = Column(String(64), nullable=False)
    birthdate = Column(Date, nullable=False)
    address = Column(String(128), nullable=False)
    phone = Column(String(32), nullable=False)
    parents_phone = Column(String(32), nullable=False)
    school = Column(String(32), nullable=False)
    enter_date = Column(Date, nullable=False)
    student_group_id = Column(
        Integer, ForeignKey("student_group.id"), unique=True)
    student_group = relationship("StudentGroup")


class Report(Base):
    """Report DAO representation."""

    __tablename__ = "report"

    id = Column(Integer, primary_key=True)
    mark = Column(Integer, nullable=False)
    mark_date = Column(Date, nullable=False)
    report_type = Column(TReport, nullable=False)
    discipline_id = Column(Integer, ForeignKey("discipline.id"), unique=True)
    student_id = Column(Integer, ForeignKey("student.id"), unique=True)
    discipline = relationship("Discipline")
    student = relationship("Student")


class Discipline(Base):
    """Discipline DAO representation."""

    __tablename__ = "discipline"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)


class StudentGroup(Base):
    """StudentGroup DAO representation."""

    __tablename__ = "student_group"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    fulltime = Column(Boolean, nullable=False)
