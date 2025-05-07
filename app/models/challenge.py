from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db_base import Base

class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(Text)
    difficulty = Column(String)  # easy, medium, hard
    testcases = relationship("TestCase", back_populates="challenge")

class TestCase(Base):
    __tablename__ = "testcases"
    id = Column(Integer, primary_key=True)
    input = Column(Text)
    expected_output = Column(Text)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    challenge = relationship("Challenge", back_populates="testcases")
