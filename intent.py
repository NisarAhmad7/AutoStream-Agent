# Converts raw user text into a simple intent label
# This helps the agent decide how to respond next
def detect_intent(user_input: str):

    text = user_input.lower()

    if "hi" in text or "hello" in text:
        return "greeting"

    elif "want" in text or "plan" in text or "price" in text:
        return "question"

    elif "sign" in text or "buy" in text or "pro plan" in text:
        return "high_intent"

    return "question"