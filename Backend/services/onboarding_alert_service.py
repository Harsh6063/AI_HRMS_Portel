from datetime import datetime

from model import (
    Alert,
    Employee,
    OnboardingTask
)

# =========================
# CHECK ONBOARDING ALERTS
# =========================

def check_onboarding_alerts(
    employee,
    db
):
    now = datetime.utcnow()

    difference = (
        now - employee.created_at
    ).total_seconds()

    # DEMO:
    # 1 day = 60 sec

    if difference > 60:
        pending_tasks = (
            db.query(OnboardingTask)
            .filter(
                OnboardingTask.employee_id
                ==
                employee.id,

                OnboardingTask.completed
                == False
            )
            .all()
        )

        if len(pending_tasks) == 0:
            return

        # EXISTING ALERT

        existing = (
            db.query(Alert)
            .filter(
                Alert.onboarding_id
                ==
                employee.id,

                Alert.resolved == False
            )
            .first()
        )

        if existing:
            return

        pending_titles = ", ".join(
            [
                task.title
                for task in pending_tasks
            ]
        )

        alert = Alert(
            onboarding_id=employee.id,

            severity="MEDIUM",

            title=
                "Employee Onboarding Delayed",

            message=(
                f"{employee.name} "
                f"still has pending "
                f"tasks: {pending_titles}"
            )
        )

        db.add(alert)

        db.commit()