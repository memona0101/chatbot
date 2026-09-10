from __future__ import annotations

import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import ChatSession


def generate_session_token() -> str:
    """Generate a secure random session token."""
    return secrets.token_urlsafe(32)


def create_session(db: Session) -> ChatSession:
    """Create a new chat session."""

    session = ChatSession(
        session_token=generate_session_token(),
        lead_state="idle",
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_session(
    db: Session,
    session_token: str,
) -> ChatSession | None:
    """Load an existing session by its server-controlled token."""

    statement = select(ChatSession).where(
        ChatSession.session_token == session_token
    )

    return db.execute(statement).scalar_one_or_none()


def get_or_create_session(
    db: Session,
    session_token: str | None = None,
) -> ChatSession:
    """Load an existing session or create a new one."""

    if session_token:
        session = get_session(db, session_token)

        if session:
            return session

    return create_session(db)
