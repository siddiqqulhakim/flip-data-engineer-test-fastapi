import httpx

POKE_API = "https://pokeapi.co/api/v2/ability/{}"

async def fetch_ability(ability_id: int):
    async with httpx.AsyncClient() as client:
        resp = await client.get(POKE_API.format(ability_id))
        resp.raise_for_status()
        return resp.json()
