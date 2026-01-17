from pydantic import BaseModel
from typing import List, Dict

class AbilityRequest(BaseModel):
    raw_id: str
    user_id: str
    pokemon_ability_id: int

class ReturnedEntry(BaseModel):
    effect: str
    language: Dict
    short_effect: str

class AbilityResponse(BaseModel):
    raw_id: str
    user_id: str
    returned_entries: List[ReturnedEntry]
    pokemon_list: List[str]
