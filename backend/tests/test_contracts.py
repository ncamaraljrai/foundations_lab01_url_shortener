from __future__ import annotations

from app.service import CODE_LENGTH, generate_code


def test_generated_short_codes_are_exactly_six_alphanumeric_characters() -> None:
    """Executable contract replacing a prose-only short-code format rule."""
    assert CODE_LENGTH == 6

    for _ in range(100):
        code = generate_code()
        assert len(code) == 6
        assert code.isalnum()
