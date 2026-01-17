from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas, services
from contextlib import asynccontextmanager
from app.models import Base, PokemonAbilityRaw, PokemonAbilityResponse



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/ability", response_model=schemas.AbilityResponse)
async def get_ability(
    data: schemas.AbilityRequest,
    db: Session = Depends(get_db)
):
    api_response = await services.fetch_ability(data.pokemon_ability_id)

    raw_record = PokemonAbilityRaw(
        raw_id=data.raw_id,
        user_id=data.user_id,
        pokemon_ability_id=data.pokemon_ability_id,
        raw_response=api_response
    )
    db.add(raw_record)

    returned_entries = []

    for entry in api_response["effect_entries"]:
        normalized_record = PokemonAbilityResponse(
            raw_id=data.raw_id,
            user_id=data.user_id,
            pokemon_ability_id=data.pokemon_ability_id,
            effect=entry["effect"],
            language=entry["language"],
            short_effect=entry["short_effect"]
        )
        db.add(normalized_record)

        returned_entries.append({
            "effect": entry["effect"],
            "language": entry["language"],
            "short_effect": entry["short_effect"]
        })

    db.commit()

    pokemon_list = [
        p["pokemon"]["name"] for p in api_response.get("pokemon", [])
    ]

    return {
        "raw_id": data.raw_id,
        "user_id": data.user_id,
        "returned_entries": returned_entries,
        "pokemon_list": pokemon_list
    }
