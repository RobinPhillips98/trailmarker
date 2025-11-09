from sqlalchemy import Column, Integer, String, ForeignKey, ARRAY, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

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
    max_hit_points = Column(JSON, nullable=False)
    immunities = Column(ARRAY(String))
    speed = Column(Integer, nullable=False)
    actions = Column(JSON)

class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(Integer, primary_key=True, index=True)
    enemies = Column(ARRAY(Integer))