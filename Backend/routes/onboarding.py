from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from database import get_db

from model import (
    Employee,
    OnboardingTask
)

from services.onboarding_alert_service import (
    check_onboarding_alerts
)

import requests

router = APIRouter(
    prefix="/onboarding",
    tags=["Onboarding"]
)

# =========================
# CREATE EMPLOYEE
# =========================

@router.post("/employee")
def create_employee(
    data: dict,
    db: Session = Depends(get_db)
):
    employee = Employee(
        name=data["name"],

        email=data["email"],

        role=data["role"],

        onboarding_status=
            "Not Started"
    )

    db.add(employee)

    db.commit()

    db.refresh(employee)

    return {
        "message":
            "Employee created"
    }

# =========================
# GET EMPLOYEES
# =========================

@router.get("/employees")
def get_employees(
    db: Session = Depends(get_db)
):
    employees = (
        db.query(Employee)
        .order_by(
            Employee.id.desc()
        )
        .all()
    )

    response = []

    for employee in employees:

        # =========================
        # TASKS
        # =========================

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

        # =========================
        # PROGRESS
        # =========================

        progress = 0

        if total_tasks > 0:
            progress = int(
                (
                    completed_tasks
                    /
                    total_tasks
                ) * 100
            )

        # =========================
        # STATUS
        # =========================

        readiness = "At Risk"

        if progress >= 100:

            readiness = (
                "Fully Onboarded"
            )

            employee.onboarding_status = (
                "Fully Onboarded"
            )

        elif progress >= 70:

            readiness = (
                "Near Ready"
            )

        elif progress >= 30:

            readiness = (
                "In Progress"
            )

        # =========================
        # PENDING TASKS
        # =========================

        pending_tasks = [
            task.title
            for task in tasks
            if not task.completed
        ]

        # =========================
        # ALERT CHECK
        # =========================

        check_onboarding_alerts(
            employee,
            db
        )

        response.append({
            "id":
                employee.id,

            "name":
                employee.name,

            "email":
                employee.email,

            "role":
                employee.role,

            "onboarding_status":
                readiness,

            "progress":
                progress,

            "completed_tasks":
                completed_tasks,

            "total_tasks":
                total_tasks,

            "pending_tasks":
                pending_tasks
        })

    db.commit()

    return response

# =========================
# START ONBOARDING
# =========================

@router.post(
    "/start/{employee_id}"
)
def start_onboarding(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.id
            ==
            employee_id
        )
        .first()
    )

    if not employee:
        return {
            "error":
                "Employee not found"
        }

    # =========================
    # EXISTING TASKS
    # =========================

    existing_tasks = (
        db.query(OnboardingTask)
        .filter(
            OnboardingTask.employee_id
            ==
            employee.id
        )
        .all()
    )

    if len(existing_tasks) > 0:
        return {
            "message":
                "Onboarding already started"
        }

    # =========================
    # ROLE BASED TASKS
    # =========================

    tasks = []

    # SOFTWARE ENGINEER

    if employee.role == "Software Engineer":

        tasks = [
            (
                "Laptop Assigned",
                "IT Team"
            ),

            (
                "GitHub Access",
                "IT Team"
            ),

            (
                "Slack Access",
                "HR Team"
            ),

            (
                "Dev Environment Setup",
                "Engineering"
            ),

            (
                "First Task Assigned",
                "Manager"
            )
        ]

    # SALES TEAM

    elif employee.role == "Sales Team":

        tasks = [
            (
                "CRM Access",
                "IT Team"
            ),

            (
                "Product Training",
                "Sales Lead"
            ),

            (
                "Territory Briefing",
                "Manager"
            ),

            (
                "Client Shadowing",
                "Sales Lead"
            )
        ]

    # OPERATIONS TEAM

    elif employee.role == "Operations Team":

        tasks = [
            (
                "Process Documentation",
                "Operations Lead"
            ),

            (
                "Reporting Access",
                "IT Team"
            ),

            (
                "Compliance Training",
                "HR Team"
            )
        ]

    # =========================
    # CREATE TASKS
    # =========================

    for title, team in tasks:

        task = OnboardingTask(
            employee_id=
                employee.id,

            title=title,

            description=
                f"{title} pending",

            assigned_team=
                team
        )

        db.add(task)

    # =========================
    # UPDATE STATUS
    # =========================

    employee.onboarding_status = (
        "In Progress"
    )

    db.commit()

    # =========================
    # SEND WELCOME MAIL
    # =========================

    try:

        response = requests.post(
            "http://127.0.0.1:8000/mail/send-welcome-mail",

            json={
                "name":
                    employee.name,

                "email":
                    employee.email,

                "role":
                    employee.role
            }
        )

        print(response.text)

    except Exception as e:
        print(e)

    return {
        "message":
            "Welcome mail sent and onboarding started"
    }

# =========================
# GET TASKS
# =========================

@router.get(
    "/employee/{employee_id}/tasks"
)
def get_tasks(
    employee_id: int,
    db: Session = Depends(get_db)
):
    tasks = (
        db.query(OnboardingTask)
        .filter(
            OnboardingTask.employee_id
            ==
            employee_id
        )
        .all()
    )

    return tasks

# =========================
# COMPLETE TASK
# =========================

@router.patch(
    "/task/{task_id}/complete"
)
def complete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(OnboardingTask)
        .filter(
            OnboardingTask.id
            ==
            task_id
        )
        .first()
    )

    if not task:
        return {
            "error":
                "Task not found"
        }

    task.completed = True

    db.commit()

    return {
        "message":
            "Task completed"
    }

# =========================
# DELETE EMPLOYEE
# =========================

@router.delete(
    "/employee/{employee_id}"
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(
            Employee.id
            ==
            employee_id
        )
        .first()
    )

    if not employee:
        return {
            "error":
                "Employee not found"
        }

    # =========================
    # DELETE TASKS
    # =========================

    tasks = (
        db.query(OnboardingTask)
        .filter(
            OnboardingTask.employee_id
            ==
            employee.id
        )
        .all()
    )

    for task in tasks:
        db.delete(task)

    # =========================
    # DELETE EMPLOYEE
    # =========================

    db.delete(employee)

    db.commit()

    return {
        "message":
            "Employee removed"
    }