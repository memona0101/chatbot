from sqlalchemy.orm import Session

from app.db.models import ChatSession, LeadCapture


IDLE = "idle"
COLLECTING_NAME = "collecting_name"
COLLECTING_EMAIL = "collecting_email"
COLLECTING_PHONE = "collecting_phone"
COMPLETE = "complete"


REQUIRED_FIELDS = [
    "full_name",
    "email",
    "contact_number",
]


def get_or_create_lead(
    db: Session,
    session: ChatSession,
) -> LeadCapture:
    if session.lead:
        return session.lead

    lead = LeadCapture(
        session_id=session.id,
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead


def get_missing_required_field(
    lead: LeadCapture,
) -> str | None:

    if not lead.full_name:
        return "full_name"

    if not lead.email:
        return "email"

    if not lead.contact_number:
        return "contact_number"

    return None


def get_next_lead_state(
    lead: LeadCapture,
) -> str:

    missing = get_missing_required_field(lead)

    if missing == "full_name":
        return COLLECTING_NAME

    if missing == "email":
        return COLLECTING_EMAIL

    if missing == "contact_number":
        return COLLECTING_PHONE

    return COMPLETE


def update_lead_state(
    db: Session,
    session: ChatSession,
) -> str:

    lead = get_or_create_lead(db, session)

    state = get_next_lead_state(lead)

    session.lead_state = state

    db.add(session)
    db.commit()
    db.refresh(session)

    return state