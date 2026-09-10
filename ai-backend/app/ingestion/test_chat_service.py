import asyncio

from app.db.database import SessionLocal
from app.services.session_manager import create_session
from app.services.chat_service import process_message


async def main():

    db = SessionLocal()

    try:
        session = create_session(db)

        print("=" * 70)
        print("SESSION")
        print("=" * 70)
        print(session.session_token)

        query = "How much does a custom website cost?"

        print("\n" + "=" * 70)
        print("USER")
        print("=" * 70)
        print(query)

        answer = await process_message(
            db,
            session=session,
            user_message=query,
        )

        print("\n" + "=" * 70)
        print("ASSISTANT")
        print("=" * 70)
        print(answer)

        print("\n" + "=" * 70)
        print("LEAD STATE")
        print("=" * 70)
        print(session.lead_state)

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())