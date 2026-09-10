from app.services.intent_router import (
    classify_intent,
    HIGH_BUYING_INTENT,
    PRICING,
    SERVICE_INQUIRY,
    NORMAL,
    FALLBACK,
)


def test_classify_empty_message():
    assert classify_intent("") == FALLBACK
    assert classify_intent("   ") == FALLBACK


def test_classify_high_buying_intent():
    assert classify_intent("I want to hire your team") == HIGH_BUYING_INTENT
    assert classify_intent("Ready to start my project") == HIGH_BUYING_INTENT
    assert classify_intent("Can you build a portal for us?") == HIGH_BUYING_INTENT


def test_classify_pricing_intent():
    assert classify_intent("How much does a website cost?") == PRICING
    assert classify_intent("What is the price of an AI chatbot?") == PRICING
    assert classify_intent("Can I get a quote?") == PRICING


def test_classify_service_inquiry():
    assert classify_intent("What services do you provide?") == SERVICE_INQUIRY
    assert classify_intent("Do you do web development?") == SERVICE_INQUIRY


def test_classify_normal():
    assert classify_intent("Hello there!") == NORMAL
    assert classify_intent("Thank you very much") == NORMAL
