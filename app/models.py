from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base

class PokemonAbilityRaw(Base):
    __tablename__ = "pokemon_ability_raw"

    id = Column(Integer, primary_key=True)
    raw_id = Column(String(13))
    user_id = Column(String(7))
    pokemon_ability_id = Column(Integer)
    raw_response = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())


class PokemonAbilityResponse(Base):
    __tablename__ = "pokemon_ability_response"

    id = Column(Integer, primary_key=True)
    raw_id = Column(String(13))
    user_id = Column(String(7))
    pokemon_ability_id = Column(Integer)
    effect = Column(Text)
    language = Column(JSON)
    short_effect = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
