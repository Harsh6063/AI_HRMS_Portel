from model import CandidateTimeline

def create_timeline_event(
    db,
    candidate_id,
    action,
    description
):
    event = CandidateTimeline(
        candidate_id=candidate_id,
        action=action,
        description=description
    )

    db.add(event)

    db.commit()