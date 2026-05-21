from database import SessionLocal
from model import Candidate

db = SessionLocal()

candidates = [
    Candidate(
        name="Rahul Sharma",
        role="Backend Engineer",
        stage="Interview",
        ai_score="92%",
        days_in_stage=5
    ),
    Candidate(
        name="Ananya Gupta",
        role="Frontend Engineer",
        stage="Screening",
        ai_score="88%",
        days_in_stage=2
    ),
    Candidate(
        name="Priya Singh",
        role="Sales Executive",
        stage="Offer",
        ai_score="81%",
        days_in_stage=1
    ),
]

for candidate in candidates:
    db.add(candidate)

db.commit()

print("Seed data added")