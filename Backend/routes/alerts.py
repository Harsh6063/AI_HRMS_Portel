from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import get_db

from model import (
    Alert,
    Candidate
)

from services.alert_service import (
    check_candidate_alert
)

from services.email_service import (
    send_resolution_email
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

# =========================
# GET ALERTS
# =========================

@router.get("/")
def get_alerts(
    db: Session = Depends(get_db)
):
    # CHECK CANDIDATES

    candidates = (
        db.query(Candidate).all()
    )

    for candidate in candidates:
        check_candidate_alert(
            candidate,
            db
        )

    return (
        db.query(Alert)
        .order_by(
            Alert.created_at.desc()
        )
        .all()
    )

# =========================
# RESOLVE ALERT
# =========================

@router.patch("/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        return {
            "error": "Alert not found"
        }

    alert.resolved = True
    candidate = (
    db.query(Candidate)
    .filter(
        Candidate.id
        ==
        alert.candidate_id
    )
    .first()
)

    if candidate:
        candidate.alert_status = "resolved"
    db.commit()

    # SEND EMAIL

    await send_resolution_email(
        alert.title,
        alert.message
    )

    return {
        "message":
            "Alert resolved successfully"
    }

# =========================
# DELETE ALERT
# =========================

@router.delete("/{alert_id}")
def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = (
        db.query(Alert)
        .filter(Alert.id == alert_id)
        .first()
    )

    if not alert:
        return {
            "error": "Alert not found"
        }
        
    candidate = (
    db.query(Candidate)
    .filter(
        Candidate.id
        ==
        alert.candidate_id
    )
    .first()
)

    if candidate:
        candidate.alert_status = "dismissed"

    db.delete(alert)

    db.commit()

    return {
        "message": "Alert deleted"
    }

    return {
        "message":
            "Alert deleted successfully"
    }
    
