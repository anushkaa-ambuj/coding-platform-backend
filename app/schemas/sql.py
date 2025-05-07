# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255))
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Challenge(Base):
    __tablename__ = 'challenges'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    input_format = Column(Text)
    output_format = Column(Text)
    sample_input = Column(Text)
    sample_output = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TestCase(Base):
    __tablename__ = 'test_cases'
    id = Column(Integer, primary_key=True)
    challenge_id = Column(Integer, ForeignKey('challenges.id'))
    input_data = Column(Text)
    expected_output = Column(Text)
    is_hidden = Column(Boolean, default=False)
    s3_key = Column(String(255), nullable=True)  # for hidden cases
    challenge = relationship("Challenge", back_populates="test_cases")

Challenge.test_cases = relationship("TestCase", back_populates="challenge")
