from fastapi import APIRouter
from app.services import generer_idees

router = APIRouter()

@router.post("/")
def get_ideas(niche: str = "bricolage"):
    return {"ideas": generer_idees(niche)}