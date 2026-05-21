from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)
import requests
from sqlalchemy.orm import Session

from database import get_db
from datetime import datetime

from model import (
    Candidate,
    CandidateTimeline,
    Employee
)

from services.scoring_service import (
    calculate_ats_score,
    extract_contact_info,
    extract_candidate_name
)

from services.timeline_service import (
    create_timeline_event
)

from services.alert_service import (
    check_candidate_alert
)

from services.ai_summary_service import (
    generate_ai_summary
)

import fitz

router = APIRouter(
    prefix="/recruitment",
    tags=["Recruitment"]
)

# =========================
# GET CANDIDATES
# =========================

@router.get("/candidates")
def get_candidates(
    db: Session = Depends(get_db)
):
    return (
        db.query(Candidate)
        .order_by(
            Candidate.id.desc()
        )
        .all()
    )

# =========================
# UPLOAD RESUME
# =========================

@router.post("/upload-resume")
async def upload_resume(
    role: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # =========================
    # READ PDF
    # =========================

    pdf_bytes = await file.read()

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    # =========================
    # ATS ANALYSIS
    # =========================

    ats = calculate_ats_score(
        text,
        role
    )

    # =========================
    # CONTACT EXTRACTION
    # =========================

    contact = extract_contact_info(
        text
    )

    # =========================
    # NAME EXTRACTION
    # =========================

    candidate_name = (
        extract_candidate_name(
            text
        )
    )

    # =========================
    # AI SUMMARY
    # =========================

    ai_summary = (
        generate_ai_summary(
            text,
            role
        )
    )

    # =========================
    # CREATE CANDIDATE
    # =========================

    candidate = Candidate(
        name=candidate_name,

        role=role,

        stage="Screening",

        ai_score=ats["score"],

        days_in_stage=1,

        strengths=ats["strengths"],

        missing_skills=
            ats["missing_skills"],

        resume_summary=
            ai_summary,

        experience_years=
            ats["experience_years"],

        communication_score=
            ats["communication_score"],

        priority=
            ats["priority"],

        email=contact["email"],

        phone=contact["phone"],

        linkedin=
            contact["linkedin"],

        resume_text=text
    )

    db.add(candidate)

    db.commit()

    db.refresh(candidate)

    # =========================
    # TIMELINE EVENT
    # =========================

    create_timeline_event(
        db,
        candidate.id,
        "Resume Uploaded",
        "Candidate resume uploaded and ATS evaluated"
    )

    # =========================
    # ALERT CHECK
    # =========================

    check_candidate_alert(
        candidate,
        db
    )

    return {
        "candidate": {
            "id": candidate.id,

            "name": candidate.name,

            "role": candidate.role,

            "stage": candidate.stage,

            "ai_score":
                candidate.ai_score,

            "days_in_stage":
                candidate.days_in_stage,

            "strengths":
                candidate.strengths,

            "missing_skills":
                candidate.missing_skills,

            "experience_years":
                candidate.experience_years,

            "communication_score":
                candidate.communication_score,

            "priority":
                candidate.priority,

            "resume_summary":
                candidate.resume_summary,

            "email":
                candidate.email
        },

        "ats": ats
    }

# =========================
# CHANGE CANDIDATE STAGE
# =========================

@router.patch(
    "/candidate/{candidate_id}/action"
)
def recruiter_action(
    candidate_id: int,
    action: str,
    db: Session = Depends(get_db)
):
    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id == candidate_id
        )
        .first()
    )

    if not candidate:
        return {
            "error":
                "Candidate not found"
        }

    # =========================
    # UPDATE STAGE
    # =========================

    candidate.stage = action

    candidate.stage_updated_at = (
        datetime.utcnow()
    )

    # =========================
    # SHORTLIST MAIL
    # =========================

    if action == "Shortlisted":

        try:
            requests.post(
                "http://127.0.0.1:8000/mail/send-shortlist-mail",

                json={
                    "email":
                        candidate.email,

                    "candidate_name":
                        candidate.name,

                    "role":
                        candidate.role
                }
            )

        except Exception as e:
            print(e)

    # =========================
    # AUTO CREATE EMPLOYEE
    # =========================

    if action == "Hired":

        existing_employee = (
            db.query(Employee)
            .filter(
                Employee.email
                ==
                candidate.email
            )
            .first()
        )

        if not existing_employee:

            employee = Employee(
                name=candidate.name,

                email=candidate.email,

                role=candidate.role,

                onboarding_status=
                    "Not Started"
            )

            db.add(employee)

    # =========================
    # TIMELINE EVENT
    # =========================

    create_timeline_event(
        db,
        candidate.id,
        action,
        f"Recruiter moved candidate to {action}"
    )

    db.commit()

    db.refresh(candidate)

    return {
        "message":
            f"Candidate moved to {action}",

        "candidate_stage":
            candidate.stage,

        "stage_updated_at":
            candidate.stage_updated_at
    }

# =========================
# GET TIMELINE
# =========================

@router.get(
    "/candidate/{candidate_id}/timeline"
)
def get_timeline(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    timeline = (
        db.query(CandidateTimeline)
        .filter(
            CandidateTimeline.candidate_id
            ==
            candidate_id
        )
        .order_by(
            CandidateTimeline.created_at.desc()
        )
        .all()
    )

    return timeline

# =========================
# DELETE CANDIDATE
# =========================

@router.delete(
    "/candidate/{candidate_id}"
)
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db)
):
    candidate = (
        db.query(Candidate)
        .filter(
            Candidate.id
            ==
            candidate_id
        )
        .first()
    )

    if not candidate:
        return {
            "error":
                "Candidate not found"
        }

    # DELETE TIMELINE

    timeline = (
        db.query(CandidateTimeline)
        .filter(
            CandidateTimeline.candidate_id
            ==
            candidate.id
        )
        .all()
    )

    for item in timeline:
        db.delete(item)

    db.delete(candidate)

    db.commit()

    return {
        "message":
            "Candidate removed"
    }