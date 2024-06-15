"""Module contains all models for the application.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 16th June 2024
Last-modified: 16th June 2024
Error-series: 2400
"""

from sqlalchemy import Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass


class Sites(Base):
    __tablename__ = "sites"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    site_name = mapped_column(String, unique=True, nullable=False)
