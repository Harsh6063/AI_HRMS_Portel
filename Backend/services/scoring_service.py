import re

def calculate_ats_score(
    resume_text: str,
    role: str
):
    text = resume_text.lower()

    # =========================
    # ROLE SKILLS
    # =========================

    role_skills = {
        "Software Engineer": [
            "python",
            "react",
            "node",
            "sql",
            "git",
            "api",
            "docker",
            "aws",
            "typescript",
            "fastapi",
            "javascript"
        ],

        "Operations Team": [
            "excel",
            "operations",
            "reporting",
            "documentation",
            "compliance",
            "coordination",
            "workflow",
            "process"
        ],

        "Sales Team": [
            "sales",
            "crm",
            "communication",
            "negotiation",
            "lead generation",
            "client handling",
            "presentation",
            "marketing"
        ]
    }

    required_skills = role_skills.get(role, [])

    matched = []

    missing = []

    # =========================
    # SKILL MATCHING
    # =========================

    for skill in required_skills:
        if skill in text:
            matched.append(skill)
        else:
            missing.append(skill)

    # =========================
    # EXPERIENCE DETECTION
    # =========================

    experience_years = 0

    experience_patterns = [
    r"(\d+)\+?\s*years?",
    r"(\d+)\+?\s*yrs?",
    r"(\d+)\+?\s*year",
    r"(\d+)-years?",
    r"(\d+)-year",
    r"experience\s+of\s+(\d+)",
    r"(\d+)\s+year\s+experience",
    r"(\d+)\s+years\s+experience",
    r"over\s+(\d+)\s+years",
    r"more\s+than\s+(\d+)\s+years",
]

    for pattern in experience_patterns:
        match = re.search(pattern, text)

        if match:
            experience_years = int(
                match.group(1)
            )

            break

    # =========================
    # COMMUNICATION ANALYSIS
    # =========================

    communication_keywords = [
        "communication",
        "leadership",
        "teamwork",
        "presentation",
        "collaboration",
        "stakeholder",
        "client",
        "management",
        "public speaking",
        "coordination"
    ]

    communication_matches = 0

    for keyword in communication_keywords:
        if keyword in text:
            communication_matches += 1

    communication_score = min(
        100,
        communication_matches * 10
    )
    
    

    # =========================
    # EXPERIENCE SCORE
    # =========================

    experience_score = min(
        100,
        experience_years * 15
    )

    # =========================
    # SKILL SCORE
    # =========================

    if len(required_skills) > 0:
        skill_score = int(
            (
                len(matched)
                /
                len(required_skills)
            ) * 100
        )
    else:
        skill_score = 0

    # =========================
    # RESUME QUALITY
    # =========================

    quality_score = 100

    if len(text.split()) < 150:
        quality_score -= 20

    if experience_years == 0:
        quality_score -= 15

    if len(matched) < 3:
        quality_score -= 15

    quality_score = max(quality_score, 40)

    # =========================
    # FINAL ATS SCORE
    # =========================

    final_score = int(
        (
            skill_score * 0.5
            +
            communication_score * 0.2
            +
            experience_score * 0.2
            +
            quality_score * 0.1
        )
    )

    final_score = min(final_score, 100)

    # =========================
    # PRIORITY
    # =========================

    priority = "Normal"

    if final_score >= 90:
        priority = "High"

    # =========================
    # SUMMARY
    # =========================

    summary = (
        f"Candidate has "
        f"{experience_years} years "
        f"of experience with strengths in "
        f"{', '.join(matched[:5])}."
    )

    # =========================
    # RETURN
    # =========================

    return {
        "score": f"{final_score}%",

        "skill_score": f"{skill_score}%",

        "communication_score":
            f"{communication_score}%",

        "experience_years":
            experience_years,

        "strengths":
            ", ".join(matched),

        "missing_skills":
        ", ".join(missing)
        if missing
        else "No major gaps detected",

        "summary":
            summary,

        "priority":
            priority
    }
    
def extract_contact_info(
    resume_text: str
):
    # EMAIL

    email_pattern = (
        r"[a-zA-Z0-9._%+-]+"
        r"@[a-zA-Z0-9.-]+"
        r"\.[a-zA-Z]{2,}"
    )

    email_match = re.search(
        email_pattern,
        resume_text
    )

    email = (
        email_match.group()
        if email_match
        else ""
    )

    # PHONE

    phone_pattern = (
        r"(\+91[\-\s]?)?"
        r"[6-9]\d{9}"
    )

    phone_match = re.search(
        phone_pattern,
        resume_text
    )

    phone = (
        phone_match.group()
        if phone_match
        else ""
    )

    # LINKEDIN

    linkedin_pattern = (
        r"(https?:\/\/)?"
        r"(www\.)?"
        r"linkedin\.com\/[^\s]+"
    )

    linkedin_match = re.search(
        linkedin_pattern,
        resume_text
    )

    linkedin = (
        linkedin_match.group()
        if linkedin_match
        else ""
    )

    return {
        "email": email,
        "phone": phone,
        "linkedin": linkedin
    }
    
def extract_candidate_name(
    resume_text: str
):
    lines = resume_text.split("\n")

    # CLEAN LINES

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if len(line) > 2:
            cleaned_lines.append(line)

    # FIRST FEW LINES
    # usually contain name

    top_lines = cleaned_lines[:10]

    blocked_words = [
        "resume",
        "developer",
        "engineer",
        "email",
        "phone",
        "linkedin",
        "github",
        "experience",
        "education",
        "skills"
    ]

    for line in top_lines:

        lower = line.lower()

        # SKIP BAD LINES

        if any(
            word in lower
            for word in blocked_words
        ):
            continue

        # NAME-LIKE CHECK

        words = line.split()

        if (
            len(words) >= 2
            and
            len(words) <= 4
        ):
            if all(
                word[0].isupper()
                for word in words
                if word[0].isalpha()
            ):
                return line

    return "Unknown Candidate"