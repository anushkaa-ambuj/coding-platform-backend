from sqlalchemy import Column, Integer, String, Text, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.mysql_db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class Challenge(Base):
    __tablename__ = 'challenges'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(Text)
    difficulty = Column(Enum('easy', 'medium', 'hard'), nullable=False)
    time_limit = Column(Integer)
    memory_limit = Column(Integer)
    test_cases = relationship("TestCase", back_populates="challenge", cascade="all, delete-orphan")


class TestCase(Base):
    __tablename__ = "public_test_cases"
    id = Column(Integer, primary_key=True, autoincrement=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    challenge = relationship("Challenge", back_populates="test_cases")
