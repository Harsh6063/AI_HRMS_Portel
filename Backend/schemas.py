from pydantic import BaseModel

# =========================
# CANDIDATES
# =========================

class CandidateCreate(BaseModel):
    name: str
    role: str

class CandidateResponse(BaseModel):
    id: int
    name: str
    role: str
    stage: str
    ai_score: str
    days_in_stage: int

    class Config:
        from_attributes = True