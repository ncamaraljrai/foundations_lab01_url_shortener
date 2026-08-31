from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class ShortenRequest(BaseModel):
    url: HttpUrl


class ShortenResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
