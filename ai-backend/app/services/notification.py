from datetime import datetime, timezone

from app.db.models import ChatMessage, LeadCapture


def build_lead_notification(
    *,
    lead: LeadCapture,
    user_question: str,
    messages: list[ChatMessage],
) -> tuple[str, str]:
    """
    Build a structured email notification for a completed lead.
    """

    timestamp = datetime.now(timezone.utc).isoformat()

    conversation_lines = []

    for message in messages:
        role = message.role.upper()

        conversation_lines.append(
            f"{role}: {message.content}"
        )

    conversation_summary = "\n".join(conversation_lines)

    subject = (
        f"New Lead: "
        f"{lead.full_name or 'Unknown'}"
    )

    body = f"""
New lead captured from MoinSystems AI chatbot.

==================================================
LEAD INFORMATION
==================================================

Full Name:
{lead.full_name or "Not provided"}

Email:
{lead.email or "Not provided"}

Contact Number:
{lead.contact_number or "Not provided"}

Company:
{lead.company_name or "Not provided"}

Service Interest:
{lead.service_interest or "Not provided"}

Project Summary:
{lead.project_summary or "Not provided"}

Timeline:
{lead.timeline or "Not provided"}

Budget Range:
{lead.budget_range or "Not provided"}

Source Page:
{lead.source_page or "Not provided"}

==================================================
USER QUESTION
==================================================

{user_question}

==================================================
CONVERSATION
==================================================

{conversation_summary}

==================================================
TIMESTAMP
==================================================

{timestamp}
""".strip()

    return subject, body
