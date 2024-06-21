"""Module contains all models for the application.

Author: Suraj Kumar Giri (@surajgirioffl)
Init-date: 16th June 2024
Last-modified: 21st June 2024
Error-series: 2400
"""

from sqlalchemy import Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, sessionmaker, Session


class Base(DeclarativeBase):
    pass


class Sites(Base):
    __tablename__ = "sites"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    site = mapped_column(String, unique=True, nullable=False)


class Prompts(Base):
    __tablename__ = "prompts"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    prompt = mapped_column(String, nullable=False, unique=True)


class Images(Base):
    __tablename__ = "images"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    image = mapped_column(String, nullable=False, unique=True)


class Output(Base):
    __tablename__ = "output"
    file_path = mapped_column(String, primary_key=True, nullable=False)
    category = mapped_column(String, nullable=False)
    site_id = mapped_column(Integer, ForeignKey(Sites.id), nullable=False)
    prompt_id = mapped_column(Integer, ForeignKey(Prompts.id), nullable=True)
    image_id = mapped_column(Integer, ForeignKey(Images.id), nullable=True)
    timestamp = mapped_column(DateTime, nullable=False)


engine = create_engine("sqlite:///ai_generator.db", echo=False)
Base.metadata.create_all(bind=engine)


def get_new_session() -> Session:
    return sessionmaker(bind=engine)()


if __name__ == "__main__":
    sites = ["pixverse", "haiper", "ideogram", "wordhero", "pixlr"]
    site_objects = [Sites(site=site) for site in sites]
    SessionClass = sessionmaker(bind=engine)
    with SessionClass() as session:
        session.add_all(site_objects)
        session.commit()
