from sqlalchemy.orm import Session

from app.db.models import ChatMessage, ChatSession


def save_message(
    db: Session,
    *,
    session: ChatSession,
    role: str,
    content: str,
    intent: str | None = None,
    lead_state: str | None = None,
) -> ChatMessage:
    message = ChatMessage(
        session_id=session.id,
        role=role,
        content=content,
        intent=intent,
        lead_state=lead_state,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def get_session_messages(
    db: Session,
    session: ChatSession,
) -> list[ChatMessage]:
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )