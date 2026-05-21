from datetime import (
    datetime,
    timedelta
)

from model import Alert

# =========================
# ALERT CHECK
# =========================

def check_candidate_alert(
    candidate,
    db
):
    # =========================
    # STOP RECREATING
    # =========================

    if (
        candidate.alert_status
        in ["resolved", "dismissed"]
    ):
        return

    now = datetime.utcnow()

    # =========================
    # HIGH ATS DELAY
    # =========================

    score = int(
        candidate.ai_score.replace(
            "%",
            ""
        )
    )

    applied_difference = (
        now - candidate.applied_at
    ).total_seconds()

    if (
        score >= 90
        and
        applied_difference > 30
    ):
        existing = (
            db.query(Alert)
            .filter(
                Alert.message.contains(
                    candidate.name
                ),

                Alert.resolved == False
            )
            .first()
        )

        if not existing:

            alert = Alert(
                candidate_id=
                    candidate.id,

                severity="HIGH",

                title=
                    "High ATS Candidate Delayed",

                message=(
                    f"{candidate.name} "
                    f"scored "
                    f"{candidate.ai_score} "
                    f"but recruiter action "
                    f"is delayed."
                )
            )

            db.add(alert)

            db.commit()

    # =========================
    # SHORTLISTED SLA
    # =========================

    if (
        candidate.stage
        ==
        "Shortlisted"
    ):
        if (
            now
            -
            candidate.stage_updated_at
        ) > timedelta(seconds=30):

            existing = (
                db.query(Alert)
                .filter(
                    Alert.message.contains(
                        candidate.name
                    ),

                    Alert.title ==
                    "Interview Scheduling Delay",

                    Alert.resolved == False
                )
                .first()
            )

            if not existing:

                alert = Alert(
                    candidate_id=
                        candidate.id,

                    severity="HIGH",

                    title=
                        "Interview Scheduling Delay",

                    message=(
                        f"{candidate.name} "
                        f"was shortlisted "
                        f"but interview "
                        f"has not been scheduled."
                    )
                )

                db.add(alert)

                db.commit()

    # =========================
    # INTERVIEW SLA
    # =========================

    if (
        candidate.stage
        ==
        "Interview"
    ):
        if (
            now
            -
            candidate.stage_updated_at
        ) > timedelta(seconds=30):

            existing = (
                db.query(Alert)
                .filter(
                    Alert.message.contains(
                        candidate.name
                    ),

                    Alert.title ==
                    "Interview Feedback Delay",

                    Alert.resolved == False
                )
                .first()
            )

            if not existing:

                alert = Alert(
                    candidate_id=
                        candidate.id,

                    severity="HIGH",

                    title=
                        "Interview Feedback Delay",

                    message=(
                        f"{candidate.name} "
                        f"is waiting for "
                        f"interview feedback."
                    )
                )

                db.add(alert)

                db.commit()

    # =========================
    # OFFER SLA
    # =========================

    if (
        candidate.stage
        ==
        "Offer"
    ):
        if (
            now
            -
            candidate.stage_updated_at
        ) > timedelta(seconds=30):

            existing = (
                db.query(Alert)
                .filter(
                    Alert.message.contains(
                        candidate.name
                    ),

                    Alert.title ==
                    "Offer Follow-up Delay",

                    Alert.resolved == False
                )
                .first()
            )

            if not existing:

                alert = Alert(
                    candidate_id=
                        candidate.id,

                    severity="MEDIUM",

                    title=
                        "Offer Follow-up Delay",

                    message=(
                        f"{candidate.name} "
                        f"is awaiting "
                        f"offer follow-up."
                    )
                )

                db.add(alert)

                db.commit()