from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import config
from backend.api.routes import (
    cases_router,
    diagnose_router,
    evidence_router,
    review_router,
    dashboard_router,
    health_router
)

app = FastAPI(
    title=config.PROJECT_NAME,
    version=config.VERSION,
    description="NETSAGE — Cisco Packet Tracer AI Troubleshooting Backend (Grok API + Deterministic Rule Engine)"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health_router)
app.include_router(cases_router)
app.include_router(evidence_router)
app.include_router(diagnose_router)
app.include_router(review_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "message": "NETSAGE AI Network Troubleshooting Engine Operational",
        "documentation": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=config.API_HOST, port=config.API_PORT, reload=True)
