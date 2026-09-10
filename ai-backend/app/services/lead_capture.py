from sqlalchemy.orm import Session

from app.db.models import ChatSession, LeadCapture
from app.services.lead_validation import (
    validate_full_name,
    validate_email,
    validate_contact_number,
)
from app.services.lead_state import update_lead_state


def get_or_create_lead(
    db: Session,
    session: ChatSession,
) -> LeadCapture:

    if session.lead:
        return session.lead

    lead = LeadCapture(session_id=session.id)

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return lead


def capture_lead_field(
    db: Session,
    session: ChatSession,
    field: str,
    value: str,
) -> tuple[bool, str]:

    value = value.strip()

    lead = get_or_create_lead(db, session)

    if field == "full_name":

        if not validate_full_name(value):
            return False, "Please provide your full name."

        lead.full_name = value

    elif field == "email":

        if not validate_email(value):
            return False, "That email address doesn't look valid. Please enter a valid email."

        lead.email = value

    elif field == "contact_number":

        if not validate_contact_number(value):
            return False, "Please provide a valid contact number."

        lead.contact_number = value

    else:
        return False, "This lead field is not supported."

    db.commit()
    db.refresh(session)

    next_state = update_lead_state(db, session)

    return True, next_state