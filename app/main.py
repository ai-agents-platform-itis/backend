from fastapi import FastAPI

from app.config import settings
from app.routers import health, campaigns, leads, dialogs, knowledge, stats, logs
from ai_core.api.app import app as ai_core_router

app = FastAPI(
    title=settings.app.name,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health.router)
app.include_router(campaigns.router)
app.include_router(leads.router)
app.include_router(dialogs.router)
app.include_router(knowledge.router)
app.include_router(stats.router)
app.include_router(logs.router)
app.include_router(ai_core_router)


@app.on_event("startup")
async def startup_event():
    print(f"🚀 {settings.app.name} запущен!")
    print("📚 Swagger docs: http://localhost:8000/docs")
    print(f"🗄️  База данных: {settings.db.host}:{settings.db.port}/{settings.db.name}")


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app.name}",
        "docs": "/docs",
        "health": "/health"
    }