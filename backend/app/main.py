from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.database import get_connection, init_db
from app.schemas import ShortenRequest, ShortenResponse
from app.service import create_or_get_short_url, find_by_short_code


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="URL Shortener API",
    version="1.0.0",
    description="FastAPI backend for the GenAI Foundations Vibe Coding lab.",
    lifespan=lifespan,
)

frontend_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:3000",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/shorten",
    response_model=ShortenResponse,
    status_code=status.HTTP_200_OK,
)
def shorten(payload: ShortenRequest, request: Request) -> ShortenResponse:
    normalized_url = str(payload.url)
    with get_connection() as conn:
        record = create_or_get_short_url(conn, normalized_url)

    base_url = os.getenv("PUBLIC_BASE_URL")
    if not base_url:
        base_url = str(request.base_url).rstrip("/")

    return ShortenResponse(
        short_code=record.short_code,
        short_url=f"{base_url.rstrip('/')}/{record.short_code}",
        original_url=record.original_url,
    )


@app.get("/{short_code}")
def redirect(short_code: str) -> RedirectResponse:
    if len(short_code) != 6 or not short_code.isalnum():
        raise HTTPException(status_code=404, detail="Short URL not found")

    with get_connection() as conn:
        record = find_by_short_code(conn, short_code)

    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(
        url=record.original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
