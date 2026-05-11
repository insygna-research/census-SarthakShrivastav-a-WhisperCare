from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.appointments import router as appointments_router
from app.api.consent import router as consent_router
from app.api.fhir import router as fhir_router
from app.api.health import router as health_router
from app.api.intake import router as intake_router
from app.api.patient import router as patient_router
from app.api.voice import router as voice_router
from app.core.config import get_settings
from app.db.session import close_database, init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_database()
    yield
    await close_database()


settings = get_settings()

app = FastAPI(
    title=settings.app.name,
    version=settings.app.version,
    description=settings.app.description,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.allowed_origins,
    allow_credentials=settings.cors.allow_credentials,
    allow_methods=settings.cors.allowed_methods,
    allow_headers=settings.cors.allowed_headers,
)

app.include_router(health_router, prefix=settings.app.api_prefix)
app.include_router(patient_router, prefix=settings.app.api_prefix)
app.include_router(consent_router, prefix=settings.app.api_prefix)
app.include_router(intake_router, prefix=settings.app.api_prefix)
app.include_router(voice_router, prefix=settings.app.api_prefix)
app.include_router(appointments_router, prefix=settings.app.api_prefix)
app.include_router(fhir_router, prefix=settings.app.api_prefix)

