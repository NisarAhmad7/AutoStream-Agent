from knowledge_base import KNOWLEDGE_BASE

def retrieve(user_input: str):

    text = user_input.lower()

    if "pro" in text:
        return KNOWLEDGE_BASE["pricing"]["pro"]

    elif "basic" in text:
        return KNOWLEDGE_BASE["pricing"]["basic"]

    elif "refund" in text:
        return KNOWLEDGE_BASE["policy"]["refund"]

    else:
        return "No relevant info found"