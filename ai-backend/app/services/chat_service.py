from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.models import ChatMessage, ChatSession

from app.services.intent_router import (
    classify_intent,
    PRICING,
    HIGH_BUYING_INTENT,
)

from app.services.retriever import retrieve

from app.services.prompts import (
    APPROVED_FALLBACK,
    build_system_prompt,
)

from app.services.lead_state import (
    get_or_create_lead,
    update_lead_state,
    COLLECTING_NAME,
    COLLECTING_EMAIL,
    COLLECTING_PHONE,
    COMPLETE,
)

from app.core.config import settings
from app.services.lead_capture import capture_lead_field
from app.services.message_manager import save_message
from app.services.llm.factory import get_llm_provider
from app.services.email_service import send_email
from app.services.notification import build_lead_notification


def lead_question(state: str) -> str | None:
    """Return the next required lead question."""

    if state == COLLECTING_NAME:
        return "To give you a more accurate estimate, may I have your full name?"

    if state == COLLECTING_EMAIL:
        return "Thanks. What is the best email address to reach you?"

    if state == COLLECTING_PHONE:
        return "Great. What is the best contact number for you?"

    return None


def lead_field_for_state(state: str) -> str | None:
    """Map the current lead state to the database field."""

    if state == COLLECTING_NAME:
        return "full_name"

    if state == COLLECTING_EMAIL:
        return "email"

    if state == COLLECTING_PHONE:
        return "contact_number"

    return None


def send_lead_notification(
    db: Session,
    session: ChatSession,
    user_question: str,
) -> None:
    """Send notification for a completed lead and track delivery safely."""

    lead = session.lead

    if not lead:
        return

    # Prevent duplicate notifications.
    if lead.delivery_status == "sent":
        return

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    subject, body = build_lead_notification(
        lead=lead,
        user_question=user_question,
        messages=messages,
    )

    try:
        result = send_email(
            subject=subject,
            body=body,
        )

        if result.success:
            lead.delivery_status = "sent"
            lead.delivery_timestamp = datetime.now(timezone.utc)
            lead.provider_message_id = result.message_id
            lead.delivery_error = None

        else:
            lead.delivery_status = "failed"
            lead.delivery_timestamp = datetime.now(timezone.utc)
            lead.delivery_error = result.error

        db.commit()

    except Exception as exc:
        # Email failure must never break the chatbot.
        lead.delivery_status = "failed"
        lead.delivery_timestamp = datetime.now(timezone.utc)
        lead.delivery_error = str(exc)[:500]

        db.commit()


async def process_message(
    db: Session,
    *,
    session: ChatSession,
    user_message: str,
) -> str:
    """
    Process one user message.

    Flow:
    1. Continue active lead capture if required.
    2. Otherwise classify intent.
    3. Save user message.
    4. Retrieve relevant knowledge.
    5. Generate grounded answer.
    6. Start lead capture when appropriate.
    7. Save assistant response.
    """

    intent = classify_intent(user_message)

    # ---------------------------------------------------------
    # 1. Continue active lead capture
    # ---------------------------------------------------------

    current_lead_field = lead_field_for_state(session.lead_state)

    if current_lead_field:

        # Save user's lead information as a chat message.
        save_message(
            db,
            session=session,
            role="user",
            content=user_message,
            intent=intent,
            lead_state=session.lead_state,
        )

        success, result = capture_lead_field(
            db=db,
            session=session,
            field=current_lead_field,
            value=user_message,
        )

        # Invalid lead information.
        if not success:

            answer = result

            save_message(
                db,
                session=session,
                role="assistant",
                content=answer,
                intent=intent,
                lead_state=session.lead_state,
            )

            return answer

        new_state = result

        # -----------------------------------------------------
        # Lead capture completed
        # -----------------------------------------------------

        if new_state == COMPLETE:

            send_lead_notification(
                db=db,
                session=session,
                user_question=user_message,
            )

            answer = (
                "Thank you! Your information has been saved successfully. "
                "Our team will review your requirements and get back to you."
            )

        else:

            question = lead_question(new_state)

            if question:
                answer = (
                    "Thanks! I've saved that information.\n\n"
                    f"{question}"
                )
            else:
                answer = "Thanks! I've saved that information."

        save_message(
            db,
            session=session,
            role="assistant",
            content=answer,
            intent=intent,
            lead_state=session.lead_state,
        )

        return answer

    # ---------------------------------------------------------
    # 2. Save normal user message
    # ---------------------------------------------------------

    save_message(
        db,
        session=session,
        role="user",
        content=user_message,
        intent=intent,
        lead_state=session.lead_state,
    )

    # ---------------------------------------------------------
    # 3. Retrieve knowledge
    # ---------------------------------------------------------

    category = "pricing" if intent == PRICING else None

    results = retrieve(
        db=db,
        query=user_message,
        category=category,
        threshold=0.0,
    )

    # ---------------------------------------------------------
    # 4. Generate grounded answer
    # ---------------------------------------------------------

    if results:

        knowledge_chunks = [
            {
                "content": result.content,
                "score": result.score,
                "document_id": result.id,
            }
            for result in results
        ]

        system_prompt = build_system_prompt(
            knowledge_chunks=knowledge_chunks,
            intent=intent,
            lead_state=session.lead_state,
        )

        provider = get_llm_provider()

        try:
            answer = await provider.generate(
                system_prompt=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_message,
                    }
                ],
            )
        except Exception as exc:
            provider_name = settings.llm_provider.lower().strip()
            if provider_name == "ollama":
                answer = (
                    "I'm temporarily unable to reach the local AI service. "
                    "Please ensure Ollama is running and try again."
                )
            else:
                answer = (
                    "I'm temporarily unable to reach the AI service. "
                    "Please try again in a moment."
                )

    else:

        answer = APPROVED_FALLBACK

    # ---------------------------------------------------------
    # 5. Start lead capture when appropriate
    # ---------------------------------------------------------

    should_capture_lead = intent in {
        PRICING,
        HIGH_BUYING_INTENT,
    }

    if should_capture_lead:

        get_or_create_lead(
            db,
            session,
        )

        state = update_lead_state(
            db,
            session,
        )

        if state != COMPLETE:

            question = lead_question(state)

            if question:
                answer = f"{answer}\n\n{question}"

    # ---------------------------------------------------------
    # 6. Save assistant response
    # ---------------------------------------------------------

    save_message(
        db,
        session=session,
        role="assistant",
        content=answer,
        intent=intent,
        lead_state=session.lead_state,
    )

    return answer