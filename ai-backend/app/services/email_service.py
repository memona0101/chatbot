import asyncio
import logging
import smtplib
import uuid
from dataclasses import dataclass
from email.message import EmailMessage

from app.core.config import settings


logger = logging.getLogger(__name__)


@dataclass
class EmailResult:
    success: bool
    message_id: str | None = None
    error: str | None = None
    attempts: int = 0


def _sanitize_error(error: Exception) -> str:
    """
    Return a safe error message that does not expose
    SMTP credentials or other secrets.
    """
    message = str(error)

    sensitive_values = [
        settings.smtp_password,
        settings.smtp_username,
    ]

    for value in sensitive_values:
        if value:
            message = message.replace(value, "[REDACTED]")

    return message[:500]


def build_email(
    *,
    subject: str,
    body: str,
    recipient: str,
) -> EmailMessage:

    message = EmailMessage()

    message["From"] = settings.smtp_from_email
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(body)

    return message


def send_email(
    *,
    subject: str,
    body: str,
    recipient: str | None = None,
) -> EmailResult:

    recipient = recipient or settings.notification_email

    if not settings.smtp_host:
        return EmailResult(
            success=False,
            error="SMTP provider is not configured.",
            attempts=0,
        )

    if not settings.smtp_from_email:
        return EmailResult(
            success=False,
            error="SMTP sender address is not configured.",
            attempts=0,
        )

    message = build_email(
        subject=subject,
        body=body,
        recipient=recipient,
    )

    max_attempts = max(1, settings.email_max_retries)

    for attempt in range(1, max_attempts + 1):

        try:
            with smtplib.SMTP(
                settings.smtp_host,
                settings.smtp_port,
                timeout=15,
            ) as server:

                if settings.email_use_tls:
                    server.starttls()

                if settings.smtp_username:
                    server.login(
                        settings.smtp_username,
                        settings.smtp_password,
                    )

                server.send_message(message)

            message_id = str(uuid.uuid4())

            logger.info(
                "email_delivery_success",
                extra={
                    "message_id": message_id,
                    "attempt": attempt,
                },
            )

            return EmailResult(
                success=True,
                message_id=message_id,
                attempts=attempt,
            )

        except (
            smtplib.SMTPException,
            OSError,
        ) as exc:

            safe_error = _sanitize_error(exc)

            logger.warning(
    "email_delivery_failed: %s",
    safe_error,
    extra={
        "attempt": attempt,
    },
)
            

            if attempt < max_attempts:
                # Small backoff before retrying.
                # 1st retry = 1 second
                # 2nd retry = 2 seconds
                time_to_wait = attempt

                # This function is synchronous, so use a
                # simple blocking sleep.
                import time

                time.sleep(time_to_wait)

            else:
                return EmailResult(
                    success=False,
                    error=safe_error,
                    attempts=attempt,
                )

    return EmailResult(
        success=False,
        error="Email delivery failed.",
        attempts=max_attempts,
    )