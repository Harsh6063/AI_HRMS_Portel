from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from services.alert_service import check_candidate_alert
from database import get_db
from services.sla_service import (
    check_candidate_sla
)

from model import (
    Candidate,
    Employee,
    Alert,
    OnboardingTask,
    CandidateTimeline
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# =========================
# DASHBOARD SUMMARY
# =========================

@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db)
):
    # =========================
    # CANDIDATES
    # =========================

    candidates = (
        db.query(Candidate)
        .all()
    )
    # =========================
# RUN SLA CHECKS
# =========================

    for candidate in candidates:
        check_candidate_sla(
        candidate,
        db
    )

    total_candidates = len(
        candidates
    )

    high_ats = len([
        c for c in candidates
        if int(
            c.ai_score.replace(
                "%",
                ""
            )
        ) >= 90
    ])

    interviews = len([
        c for c in candidates
        if c.stage == "Interview"
    ])

    offers = len([
        c for c in candidates
        if c.stage == "Offer"
    ])

    hired = len([
        c for c in candidates
        if c.stage == "Hired"
    ])

    # =========================
    # HIRING FUNNEL
    # =========================

    applied = len([
        c for c in candidates
        if c.stage == "Screening"
    ])

    interview_stage = len([
        c for c in candidates
        if c.stage == "Interview"
    ])

    offer_stage = len([
        c for c in candidates
        if c.stage == "Offer"
    ])

    hired_stage = len([
        c for c in candidates
        if c.stage == "Hired"
    ])

    # =========================
    # EMPLOYEES
    # =========================

    employees = (
        db.query(Employee)
        .all()
    )

    onboarding_started = len([
        e for e in employees
        if e.onboarding_status
        != "Not Started"
    ])

    fully_onboarded = len([
        e for e in employees
        if e.onboarding_status
        == "Fully Onboarded"
    ])

    pending_onboarding = len([
        e for e in employees
        if e.onboarding_status
        != "Fully Onboarded"
    ])

    # =========================
    # WORKFORCE READINESS
    # =========================

    readiness_scores = []

    for employee in employees:
        tasks = (
            db.query(OnboardingTask)
            .filter(
                OnboardingTask.employee_id
                ==
                employee.id
            )
            .all()
        )

        total_tasks = len(tasks)

        completed_tasks = len([
            task
            for task in tasks
            if task.completed
        ])

        progress = 0

        if total_tasks > 0:
            progress = int(
                (
                    completed_tasks
                    /
                    total_tasks
                ) * 100
            )

        readiness_scores.append(
            progress
        )

    avg_readiness = 0

    if len(readiness_scores) > 0:
        avg_readiness = int(
            sum(readiness_scores)
            /
            len(readiness_scores)
        )

    # =========================
    # ALERTS
    # =========================

    alerts = (
        db.query(Alert)
        .filter(
            Alert.resolved == False
        )
        .all()
    )

    total_alerts = len(alerts)

    critical_alerts = len([
        a for a in alerts
        if a.severity == "HIGH"
    ])

    # =========================
    # AI INSIGHTS
    # =========================

    insights = []

    if high_ats > 3:
        insights.append(
            "High quality candidate pipeline detected."
        )

    if (
        pending_onboarding
        >
        fully_onboarded
    ):
        insights.append(
            "Onboarding delays increasing across workforce."
        )

    if critical_alerts > 0:
        insights.append(
            "Critical operational alerts require immediate attention."
        )

    if avg_readiness < 60:
        insights.append(
            "Overall workforce readiness below recommended threshold."
        )

    if interviews > offers:
        insights.append(
            "Interview conversion opportunity detected."
        )

    # =========================
    # RECENT TIMELINE
    # =========================

    timeline = (
        db.query(
            CandidateTimeline
        )
        .order_by(
            CandidateTimeline.created_at.desc()
        )
        .limit(8)
        .all()
    )

    # =========================
    # SLA MONITORING
    # =========================

    sla_issues = []

    for candidate in candidates:
        check_candidate_alert(
    candidate,
    db
)
        check_candidate_sla(candidate, db)

        if (
            candidate.stage
            ==
            "Interview"
            and
            candidate.days_in_stage
            >= 3
        ):
            sla_issues.append(
                {
                    "title":
                        "Interview Delay",

                    "message":
                        f"{candidate.name} "
                        f"stuck in interview stage"
                }
            )

    for employee in employees:

        if (
            employee.onboarding_status
            !=
            "Fully Onboarded"
        ):
            sla_issues.append(
                {
                    "title":
                        "Onboarding Delay",

                    "message":
                        f"{employee.name} "
                        f"onboarding incomplete"
                }
            )

    # =========================
    # RETURN
    # =========================

    return {
        "total_candidates":
            total_candidates,

        "high_ats":
            high_ats,

        "interviews":
            interviews,

        "offers":
            offers,

        "hired":
            hired,

        "onboarding_started":
            onboarding_started,

        "fully_onboarded":
            fully_onboarded,

        "pending_onboarding":
            pending_onboarding,

        "avg_readiness":
            avg_readiness,

        "total_alerts":
            total_alerts,

        "critical_alerts":
            critical_alerts,

        "alerts": [
            {
                "id": a.id,

                "title": a.title,

                "message": a.message,

                "severity": a.severity
            }
            for a in alerts
        ],

        "insights":
            insights,

        "funnel": {
            "Applied":
                applied,

            "Interview":
                interview_stage,

            "Offer":
                offer_stage,

            "Hired":
                hired_stage
        },

        "timeline": [
            {
                "event":
                    t.action,

                "description":
                    t.description
            }
            for t in timeline
        ],

        "sla_issues":
            sla_issues
    }