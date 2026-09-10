import re


NORMAL = "normal"
SERVICE_INQUIRY = "service_inquiry"
PRICING = "pricing"
HIGH_BUYING_INTENT = "high_buying_intent"
FALLBACK = "fallback"


def classify_intent(message: str) -> str:
    text = message.lower().strip()

    if not text:
        return FALLBACK

    # High buying intent should be checked first
    high_intent_patterns = [
        r"\bi want to hire\b",
        r"\bwant to build\b",
        r"\bready to start\b",
        r"\bstart my project\b",
        r"\bget started\b",
        r"\bbook a call\b",
        r"\bcontact (your|the) team\b",
        r"\bneed (you|your team) to build\b",
        r"\bcan you build\b",
    ]

    if any(re.search(pattern, text) for pattern in high_intent_patterns):
        return HIGH_BUYING_INTENT

    pricing_patterns = [
        r"\bprice\b",
        r"\bpricing\b",
        r"\bcost\b",
        r"\bhow much\b",
        r"\bquote\b",
        r"\bbudget\b",
        r"\bestimate\b",
    ]

    if any(re.search(pattern, text) for pattern in pricing_patterns):
        return PRICING

    service_patterns = [
        r"\bwhat services\b",
        r"\bservices do you provide\b",
        r"\bwhat do you offer\b",
        r"\bwhat can you build\b",
        r"\bservices\b",
        r"\bwebsite development\b",
        r"\bweb development\b",
        r"\bai chatbot\b",
        r"\bchatbot development\b",
    ]

    if any(re.search(pattern, text) for pattern in service_patterns):
        return SERVICE_INQUIRY

    normal_patterns = [
        r"\bhello\b",
        r"\bhi\b",
        r"\bhey\b",
        r"\bthanks\b",
        r"\bthank you\b",
        r"\bhow are you\b",
    ]

    if any(re.search(pattern, text) for pattern in normal_patterns):
        return NORMAL

    # General questions can still be handled as normal.
    return NORMAL