from fastapi import APIRouter

from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig
)


from pydantic import BaseModel

import os

router = APIRouter(
    prefix="/mail",
    tags=["Mail"]
)

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_USERNAME"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

class InterviewMail(BaseModel):
    email: str
    candidate_name: str
    date: str
    time: str
    meeting_link: str

@router.post("/send-interview-mail")
async def send_interview_mail(
    data: InterviewMail
):
    body = f"""
<html>
<body style="
font-family: Arial;
background: #0f172a;
padding: 30px;
color: white;
">

<div style="
max-width: 600px;
margin: auto;
background: #111827;
padding: 40px;
border-radius: 16px;
">

<h2 style="color:#14b8a6;">
Interview Invitation
</h2>

<p>
Hi {data.candidate_name},
</p>

<p>
We reviewed your profile and
would like to invite you for
an interview.
</p>

<div style="
background:#1F2937;
padding:20px;
border-radius:12px;
margin-top:20px;
">

<p>
<strong>Date:</strong>
{data.date}
</p>

<p>
<strong>Time:</strong>
{data.time}
</p>

<p>
<strong>Meeting Link:</strong>
<br/>
<a href="{data.meeting_link}">
{data.meeting_link}
</a>
</p>

</div>

<p style="margin-top:30px;">
Please confirm your availability.
</p>

<p>
Regards,
<br/>
Recruitment Team
</p>

</div>

</body>
</html>
"""

    message = MessageSchema(
        subject="Interview Invitation",

        recipients=[data.email],

        body=body,

        subtype="html"
    )

    fm = FastMail(conf)

    await fm.send_message(message)

    return {
        "message": "Mail sent successfully"
    }
    
# =========================
# SHORTLIST MAIL
# =========================

@router.post(
    "/send-shortlist-mail"
)
async def send_shortlist_mail(
    data: dict
):
    html = f"""
    <div style="
        font-family: Arial;
        padding: 20px;
        background: #0F172A;
        color: white;
    ">

        <h2 style="
            color: #22D3EE;
        ">
            SaarthiHR Recruitment
        </h2>

        <p>
            Hi {data["candidate_name"]},
        </p>

        <p>
            Thank you for applying for the
            <b>{data["role"]}</b>
            role.
        </p>

        <p>
            We reviewed your profile and are
            pleased to inform you that you
            have been shortlisted for the
            next stage of our hiring process.
        </p>

        <p>
            Our recruitment team will soon
            share interview details and
            next steps with you.
        </p>

        <p>
            We appreciate your interest in
            joining our organization.
        </p>

        <br>

        <p>
            Regards,
        </p>

        <p>
            Recruitment Team
            <br>
            SaarthiHR
        </p>

    </div>
    """

    message = MessageSchema(
        subject=
            "Application Shortlisted",

        recipients=[
            data["email"]
        ],

        body=html,

        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

    return {
        "message":
            "Shortlist mail sent"
    }
    
# =========================
# WELCOME MAIL
# =========================

@router.post(
    "/send-welcome-mail"
)
async def send_welcome_mail(
    data: dict
):
    html = f"""
    <div style="
        font-family: Arial;
        padding: 24px;
        background: #0F172A;
        color: white;
    ">

        <h1 style="
            color: #22D3EE;
        ">
            Welcome to HR
        </h1>

        <p>
            Hi {data["name"]},
        </p>

        <p>
            Welcome to the
            <b>{data["role"]}</b>
            team.
        </p>

        <p>
            Your onboarding process
            has officially started.
        </p>

        <div style="
            margin-top: 20px;
            padding: 16px;
            border-radius: 12px;
            background: #111827;
        ">

            <h3>
                Your Initial Checklist
            </h3>

            <ul>
                <li>
                    Complete onboarding tasks
                </li>

                <li>
                    Set up company accounts
                </li>

                <li>
                    Connect with your manager
                </li>

                <li>
                    Review company policies
                </li>
            </ul>

        </div>

        <p style="
            margin-top: 20px;
        ">
            We are excited to have you onboard.
        </p>

        <br>

        <p>
            Regards,
        </p>

        <p>
            HR Team
            <br>
            SaarthiHR
        </p>

    </div>
    """

    message = MessageSchema(
        subject=
            "Welcome to SaarthiHR",

        recipients=[
            data["email"]
        ],

        body=html,

        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(
        message
    )

    return {
        "message":
            "Welcome mail sent"
    }