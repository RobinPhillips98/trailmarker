from sqlalchemy import ARRAY, JSON, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    encounters = relationship("Encounter", back_populates="user")


class Enemy(Base):
    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    level = Column(Integer, nullable=False)
    traits = Column(ARRAY(String), nullable=False)
    perception = Column(Integer, nullable=False)
    skills = Column(JSON, nullable=False)
    attribute_modifiers = Column(JSON, nullable=False)
    defenses = Column(JSON, nullable=False)
    max_hit_points = Column(Integer, nullable=False)
    immunities = Column(ARRAY(String))
    speed = Column(Integer, nullable=False)
    actions = Column(JSON)


class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="encounters")
    name = Column(String)
    enemies = Column(JSON)
