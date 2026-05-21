from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from database import Base
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from datetime import datetime

stage_updated_at = Column(
    DateTime(timezone=True),
    server_default=func.now(),
    onupdate=func.now()
)

# =========================
# JOBS
# =========================

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    department = Column(String)

    status = Column(String)

# =========================
# CANDIDATES
# =========================

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    role = Column(String)

    stage = Column(String)

    ai_score = Column(String)

    days_in_stage = Column(Integer)

    strengths = Column(String)

    missing_skills = Column(String)

    resume_summary = Column(String)

    experience_years = Column(Integer)

    communication_score = Column(String)

    priority = Column(String)
    
    email = Column(String)

    phone = Column(String)

    linkedin = Column(String)

    applied_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    alert_status = Column(
    String,
    default="active"
)
    resume_text = Column(Text)
    
    stage_updated_at = Column(
    DateTime,
    nullable=True
)

# =========================
# EMPLOYEES
# =========================

# =========================
# EMPLOYEE
# =========================

class Employee(Base):
    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    email = Column(String)

    role = Column(String)

    onboarding_status = Column(
        String,
        default="In Progress"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

# =========================
# ONBOARDING TASKS
# =========================

class OnboardingTask(Base):
    __tablename__ = "onboarding_tasks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(Integer)

    title = Column(String)

    description = Column(String)

    completed = Column(
        Boolean,
        default=False
    )

    assigned_team = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
# =========================
# ALERTS
# =========================


    
class Alert(Base):
    __tablename__ = "alerts"
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidate_id = Column(Integer)

    severity = Column(String)

    title = Column(String)

    message = Column(String)

    resolved = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    onboarding_id = Column(
    Integer,
    nullable=True
)
    
    
class CandidateTimeline(Base):
    __tablename__ = "candidate_timeline"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    candidate_id = Column(Integer)

    action = Column(String)

    description = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )