from __future__ import annotations

import secrets
import sqlite3
import string
from dataclasses import dataclass

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6
MAX_CODE_GENERATION_ATTEMPTS = 20


@dataclass(frozen=True)
class ShortUrlRecord:
    original_url: str
    short_code: str


def generate_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


def find_by_original_url(
    conn: sqlite3.Connection, original_url: str
) -> ShortUrlRecord | None:
    row = conn.execute(
        "SELECT original_url, short_code FROM urls WHERE original_url = ?",
        (original_url,),
    ).fetchone()
    if not row:
        return None
    return ShortUrlRecord(
        original_url=row["original_url"],
        short_code=row["short_code"],
    )


def find_by_short_code(
    conn: sqlite3.Connection, short_code: str
) -> ShortUrlRecord | None:
    row = conn.execute(
        "SELECT original_url, short_code FROM urls WHERE short_code = ?",
        (short_code,),
    ).fetchone()
    if not row:
        return None
    return ShortUrlRecord(
        original_url=row["original_url"],
        short_code=row["short_code"],
    )


def create_or_get_short_url(
    conn: sqlite3.Connection, original_url: str
) -> ShortUrlRecord:
    existing = find_by_original_url(conn, original_url)
    if existing:
        return existing

    for _ in range(MAX_CODE_GENERATION_ATTEMPTS):
        code = generate_code()
        try:
            conn.execute(
                "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
                (original_url, code),
            )
            conn.commit()
            return ShortUrlRecord(original_url=original_url, short_code=code)
        except sqlite3.IntegrityError:
            # Could be a short-code collision or concurrent insert.
            duplicate = find_by_original_url(conn, original_url)
            if duplicate:
                return duplicate

    raise RuntimeError("Could not generate a unique short code.")
