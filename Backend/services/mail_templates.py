def generate_mail(
    candidate_name,
    action
):
    templates = {
        "Interview":
            f"""
Hi {candidate_name},

We reviewed your profile and would like to schedule an interview with you.

Please share your availability.

Regards,
Recruitment Team
""",

        "Reject":
            f"""
Hi {candidate_name},

Thank you for your interest.

After careful review, we will not be moving forward.

Regards,
Recruitment Team
""",

        "Offer":
            f"""
Hi {candidate_name},

Congratulations!

We are excited to move forward with an offer.

Regards,
Recruitment Team
"""
    }

    return templates.get(
        action,
        ""
    )