from datetime import (
    datetime,
    timedelta
)

from model import Alert

# =========================
# CHECK SLA
# =========================

def check_candidate_sla(
    candidate,
    db
):
    if not candidate.stage_updated_at:
        return

    now = datetime.utcnow()

    difference = (
        now -
        candidate.stage_updated_at
    )

    print(
        candidate.name,
        candidate.stage,
        difference.seconds
    )

    # =========================
    # SHORTLISTED
    # =========================

    if (
        candidate.stage
        ==
        "Shortlisted"
        and
        difference
        >
        timedelta(seconds=10)
    ):

        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.message.contains(
                    candidate.name
                )
            )
            .first()
        )

        if not existing_alert:

            alert = Alert(
                title=
                    "Interview Scheduling Delay",

                message=
                    f"{candidate.name} shortlisted but interview not scheduled.",

                severity="HIGH",

                resolved=False
            )

            db.add(alert)

            db.commit()

            print(
                "SHORTLIST ALERT CREATED"
            )

    # =========================
    # INTERVIEW
    # =========================

    if (
        candidate.stage
        ==
        "Interview"
        and
        difference
        >
        timedelta(seconds=30)
    ):

        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.message.contains(
                    candidate.name
                )
            )
            .first()
        )

        if not existing_alert:

            alert = Alert(
                title=
                    "Interview Feedback Delay",

                message=
                    f"{candidate.name} interview feedback pending.",

                severity="HIGH",

                resolved=False
            )

            db.add(alert)

            db.commit()

            print(
                "INTERVIEW ALERT CREATED"
            )