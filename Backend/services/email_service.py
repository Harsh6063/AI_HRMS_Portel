from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig
)

from dotenv import load_dotenv

import os

load_dotenv()

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

# =========================
# SEND RESOLUTION EMAIL
# =========================

async def send_resolution_email(
    alert_title: str,
    alert_message: str
):
    message = MessageSchema(
        subject="Alert Resolved Successfully",

        recipients=[
            "admin@saarthihr.com"
        ],

        body=f"""
        <h2>Operational Alert Resolved</h2>

        <p>
        <strong>Alert:</strong>
        {alert_title}
        </p>

        <p>
        <strong>Details:</strong>
        {alert_message}
        </p>

        <p>
        Status changed to RESOLVED.
        </p>
        """,

        subtype="html"
    )

    fm = FastMail(conf)

    await fm.send_message(message)