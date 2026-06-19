from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.features.candles.router import router as candles_router
from app.features.health.router import router as health_router
from app.features.markets.router import router as markets_router
from app.features.training_sessions.router import router as training_sessions_router

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(markets_router, prefix=settings.api_prefix)
app.include_router(candles_router, prefix=settings.api_prefix)
app.include_router(training_sessions_router, prefix=settings.api_prefix)
