from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import alerts
from routes import mail
from routes import onboarding
from routes import dashboard


from database import engine
from model import Base

from routes import recruitment

# =========================
# CREATE TABLES
# =========================

Base.metadata.create_all(bind=engine)

# =========================
# APP
# =========================

app = FastAPI()

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTES
# =========================

app.include_router(recruitment.router)
app.include_router(mail.router)
# =========================
# ROOT
# =========================

@app.get("/")
def root():
    return {
        "message": "SaarthiHR Backend Running"
    }
    
app.include_router(alerts.router)
app.include_router(
    onboarding.router
)

app.include_router(
    dashboard.router
)