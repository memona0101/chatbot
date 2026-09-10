from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.schemas.chat import (
    CreateSessionResponse,
    LeadCaptureRequest,
    LeadCaptureResponse,
    ChatRequest,
    ChatResponse,
)

from app.services.session_manager import (
    create_session,
    get_session,
)

from app.services.lead_capture import capture_lead_field
from app.services.chat_service import process_message, send_lead_notification, lead_question
from app.services.lead_state import COMPLETE


router = APIRouter(
    prefix="/api/v1",
    tags=["chat"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ============================================================
# CREATE CHAT SESSION
# ============================================================

@router.post(
    "/sessions",
    response_model=CreateSessionResponse,
)
def create_chat_session(
    db: Session = Depends(get_db),
):
    session = create_session(db)

    return CreateSessionResponse(
        session_token=session.session_token,
        lead_state=session.lead_state,
    )


# ============================================================
# CHAT
# ============================================================

@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    session = get_session(
        db,
        request.session_token,
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    answer = await process_message(
        db=db,
        session=session,
        user_message=request.message,
    )

    return ChatResponse(
        session_token=session.session_token,
        message=answer,
        lead_state=session.lead_state,
    )


# ============================================================
# LEAD CAPTURE
# ============================================================

@router.post(
    "/lead-capture",
    response_model=LeadCaptureResponse,
)
def lead_capture(
    request: LeadCaptureRequest,
    db: Session = Depends(get_db),
):
    session = get_session(
        db,
        request.session_token,
    )

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Session not found",
        )

    success, result = capture_lead_field(
        db=db,
        session=session,
        field=request.field,
        value=request.value,
    )

    if not success:
        return LeadCaptureResponse(
            success=False,
            message=result,
            lead_state=session.lead_state,
        )

    if result == COMPLETE:
        send_lead_notification(
            db=db,
            session=session,
            user_question="Lead submitted via chat widget",
        )

        return LeadCaptureResponse(
            success=True,
            message=(
                "Thank you! Your information has been saved successfully. "
                "Our team will review your requirements and get back to you."
            ),
            lead_state=result,
        )

    question = lead_question(result)
    message = (
        f"Thanks! I've saved that information.\n\n{question}"
        if question
        else "Thanks! I've saved that information."
    )

    return LeadCaptureResponse(
        success=True,
        message=message,
        lead_state=result,
    )