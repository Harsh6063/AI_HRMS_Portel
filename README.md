# HR — AI Powered Workforce Operations Intelligence Platform

## Overview

HR is an AI-powered workforce operations intelligence platform designed to intelligently manage the employee lifecycle from recruitment to onboarding.

The platform combines:

- AI Resume Intelligence
- ATS Scoring
- Recruitment Workflow Automation
- Onboarding Intelligence
- SLA Monitoring
- Operational Alerts
- Executive Dashboards

to improve hiring efficiency, onboarding readiness, and workforce operational visibility.

Unlike traditional HRMS systems that mainly store employee records, SaarthiHR focuses on:

> Operational Intelligence + Workflow Monitoring

---

# Problem Statement

Traditional HR and recruitment systems face several operational challenges:

## Recruitment Challenges

- Manual resume screening is time-consuming
- High-quality candidates often receive delayed responses
- Candidate ghosting increases due to poor communication
- No intelligent candidate prioritization
- Lack of operational visibility

## Onboarding Challenges

- Onboarding is often unstructured
- HR teams manually track onboarding tasks
- Infrastructure setup delays reduce productivity
- No onboarding readiness visibility
- Delayed onboarding activities go unnoticed

## Operational Challenges

- No SLA monitoring
- No intelligent workflow alerts
- Delays are detected too late
- Lack of executive-level visibility

---

# Proposed Solution

SaarthiHR solves these challenges by building:

> An AI-powered operational intelligence layer over recruitment and onboarding workflows.

The platform:

- automatically analyzes resumes using AI
- scores candidates using ATS intelligence
- tracks recruitment stages
- generates recruiter-ready candidate summaries
- automates communication workflows
- manages onboarding readiness
- monitors SLA delays
- creates operational alerts
- provides executive workforce dashboards

---

# Core Modules

# 1. Recruitment Intelligence Module

Handles:
- resume analysis
- ATS scoring
- recruitment workflow management
- interview coordination
- AI resume summaries

## Features

- Resume upload
- PDF resume parsing
- AI ATS scoring
- Role-based skill matching
- Experience extraction
- Communication scoring
- AI-generated resume summaries using Groq LLM
- Candidate stage tracking
- Timeline tracking
- Interview scheduling
- Automated shortlist mails
- Automated interview mails
- Candidate SLA monitoring

---

# 2. Onboarding Intelligence Module

Handles:
- employee onboarding
- task management
- workforce readiness monitoring
- onboarding risk detection

## Features

- Role-based onboarding tasks
- Start onboarding workflows
- Automated welcome mails
- Task completion tracking
- Readiness scoring
- Risk alerts
- Operational onboarding monitoring
- Employee lifecycle tracking

---

# System Workflow

```text
Resume Upload
        ↓
AI Resume Analysis
        ↓
ATS Scoring
        ↓
Recruitment Workflow
        ↓
Interview Coordination
        ↓
Candidate Hired
        ↓
Employee Creation
        ↓
Onboarding Started
        ↓

Welcome Mail Sent
        ↓
Task Tracking
        ↓
Operational Readiness Monitoring

```

# AI Features

## AI Resume Intelligence

The platform uses:

- Groq API
- Llama 3.1 8B Model

to generate:

- recruiter-ready summaries
- communication analysis
- hiring recommendations
- technical strengths
- missing skills analysis

This significantly reduces manual resume review effort.

---

# SLA Monitoring

The system continuously monitors:

- shortlisted candidates
- interview delays
- onboarding delays
- operational bottlenecks

and automatically generates alerts when workflows exceed predefined thresholds.

---

# AI Candidate Analysis

The AI-powered ATS engine evaluates resumes based on:

- role-specific skills
- experience patterns
- communication indicators
- technical keyword matching
- hiring readiness

The system automatically calculates:
- ATS Match Score
- Experience Score
- Communication Score
- Candidate Priority

---

# AI Resume Summaries

Recruiters can instantly view:

- candidate strengths
- missing skills
- communication assessment
- hiring recommendations
- role alignment summaries

without manually reading full resumes.

---

# Operational Intelligence

The platform intelligently tracks:
- recruitment workflows
- onboarding readiness
- delayed actions
- SLA breaches
- workforce bottlenecks

and generates real-time operational alerts.

---

# AI Workflow Automation

The platform automates:

- shortlist mails
- interview scheduling mails
- onboarding welcome mails
- operational delay alerts
- recruitment workflow tracking

reducing manual HR operational effort.

---

# Workforce Readiness Intelligence

The onboarding engine continuously evaluates:

- onboarding task completion
- infrastructure readiness
- pending operational blockers
- employee onboarding risk levels

to predict workforce operational readiness.

# AI Hiring Prioritization

The system automatically prioritizes candidates using:

- ATS scores
- communication quality
- experience relevance
- workflow delays
- role alignment

This helps recruiters focus on high-potential candidates faster and reduces delays in the hiring pipeline.

Candidates are categorized into priority levels such as:

- HIGH PRIORITY
- MEDIUM PRIORITY
- LOW PRIORITY

based on their resume intelligence and operational hiring readiness.

The prioritization engine improves recruiter efficiency by ensuring high-quality candidates receive faster attention and reduced workflow delays.

## 🛠️ Technologies Used & System Architecture

### Frontend
| Technology | Purpose |
| :--- | :--- |
| **Next.js** | Scalable frontend framework for modern production routing |
| **React.js** | Component-based, interactive user interfaces |
| **Tailwind CSS** | Utility-first styling engine for modern, responsive enterprise UIs |
| **Axios** | Promise-based asynchronous HTTP client for API communication |

### Backend
| Technology | Purpose |
| :--- | :--- |
| **FastAPI** | High-performance, asynchronous REST backend endpoints |
| **SQLAlchemy** | Object-Relational Mapping (ORM) database abstraction layer |
| **PostgreSQL** | Enterprise-grade, stable relational database instance |
| **Uvicorn** | High-velocity ASGI server to host the backend application |

### AI / NLP / Resume Processing
| Technology | Purpose |
| :--- | :--- |
| **Groq API** | Ultra-fast, low-latency AI inference execution pipeline |
| **Llama 3.1 8B** | Primary open-weights LLM utilized for parsing and resume intelligence |
| **PyMuPDF (fitz)** | Highly efficient layout-aware text extraction from PDF files |
| **Regex** | Pattern matching expressions for extracting phone numbers and emails |
| **Custom ATS Engine** | Algorithmic candidate parsing and dynamic scoring logic |

### Email Automation
| Technology | Purpose |
| :--- | :--- |
| **FastAPI-Mail** | Integrated async mail service framework engine |
| **Gmail SMTP** | Reliable transactional gateway for secure email transmission |

---

### 📐 System Architecture Diagram

```text
                ┌────────────────────┐
                │   Frontend UI      │
                │  Next.js + React   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │   FastAPI Backend  │
                │ Recruitment APIs   │
                │ Onboarding APIs    │
                │ Dashboard APIs     │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ PostgreSQL   │  │ Groq AI API  │  │ Gmail SMTP   │
│ Database     │  │ LLM Engine   │  │ Mail Service │
└──────────────┘  └──────────────┘  └──────────────┘

```

Database Tables
Core relational datasets are partitioned into five system-managed tracking tables:

candidates — Resume parsing attributes, contact details, and core metrics.

candidate_timeline — Historical step transitions across the intake workflow.

employees — Hired candidate profiles converted to internal personnel records.

onboarding_tasks — Checklists, assignments, and progression trackers for new hires.

alerts — Chronological log of operational bottlenecks and SLA threshold violations.


🚀 Installation & Setup Guide
1. Backend Configuration
Navigate to the backend module directory, set up your Python packages, and boot the application engine:

Bash 
```
cd backend
```


# Install production dependencies
```
pip install -r requirements.txt
```

# Launch the FastAPI application using Uvicorn
```
uvicorn main:app --reload
```

Backend Environment Variables (backend/.env)
Create an environment file inside your backend root folder containing the following configuration keys:

Code snippet
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/saarthihr
GROQ_API_KEY=your_groq_api_key
MAIL_USERNAME=yourgmail@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_FROM=yourgmail@gmail.com
```
2. Frontend Configuration
Navigate to your frontend application source code folder, download the Node modules, and launch the UI engine:

Bash
# Enter the frontend directory
```
cd frontend
```

# Install client packages
```
npm install
```

# Initialize the Next.js development client
```
npm run dev
```
#  Future Enhancements


[ ] Dynamic Interview Prep: AI generation of distinct interview questions custom-tailored to a candidate's resume gaps.

[ ] Comparative Analytics: Side-by-side AI candidate alignment evaluations.

[ ] Onboarding Copilot: Interactive, conversational assistant to support new hires during onboarding.

[ ] Security Controls: Deep role-based authorization rules (RBAC) across departments.

[ ] Live Notifications: Real-time push updates for urgent SLA breaches.

[ ] Advanced Search Operations: Semantic vector indexing for contextual, natural language resume search.

[ ] Multi-Tenancy Framework: Clean database partitioning to support multi-company software deployments.


