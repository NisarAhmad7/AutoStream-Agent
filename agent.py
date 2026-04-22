from langgraph.graph import StateGraph, END
from knowledge_base import KNOWLEDGE_BASE


# ---------------- INTENT ----------------
def detect_intent(text: str):
    text = text.lower()

    if any(x in text for x in ["hi", "hello", "hey"]):
        return "greeting"

    if any(x in text for x in ["price", "plan", "cost", "basic", "pro"]):
        return "question"

    if any(x in text for x in ["sign me up", "buy", "subscribe", "want pro", "want basic"]):
        return "high_intent"

    return "question"


# Retrieves relevant information from the local knowledge base
# This simulates a real RAG system without external APIs
def retrieve(text: str):
    text = text.lower()

    if "pro" in text:
        return KNOWLEDGE_BASE["pricing"]["pro"]

    if "basic" in text:
        return KNOWLEDGE_BASE["pricing"]["basic"]

    return KNOWLEDGE_BASE["policy"]


# First step in the agent flow
# It analyzes user input and stores the detected intent in state
def intent_node(state):
    state["intent"] = detect_intent(state["user_input"])
    return state


# Fetches relevant product or policy information
# Based on user input, it prepares data for the response step
def rag_node(state):
    state["retrieved"] = retrieve(state["user_input"])
    return state


# Main response generator
# Converts raw data into human-readable messages
# Also decides if user should move to lead collection step
def response_node(state):

    intent = state["intent"]
    data = state["retrieved"]

    if intent == "greeting":
        print("Agent: Hello 👋 How can I help you?")

    elif intent == "question":

        # ✅ make response HUMAN readable (fix your issue)
        if "price" in state["user_input"].lower() or "plan" in state["user_input"].lower():

            print("Agent: Here are our plans:")

            print("\nBasic Plan:")
            print(f"- Price: {KNOWLEDGE_BASE['pricing']['basic']['price']}")
            print(f"- Videos: {KNOWLEDGE_BASE['pricing']['basic']['videos']}")
            print(f"- Resolution: {KNOWLEDGE_BASE['pricing']['basic']['resolution']}")

            print("\nPro Plan:")
            print(f"- Price: {KNOWLEDGE_BASE['pricing']['pro']['price']}")
            print(f"- Videos: {KNOWLEDGE_BASE['pricing']['pro']['videos']}")
            print(f"- Resolution: {KNOWLEDGE_BASE['pricing']['pro']['resolution']}")
            print(f"- Features: {KNOWLEDGE_BASE['pricing']['pro']['features']}")

        else:
            print("Agent:", data)

    elif intent == "high_intent":
        print("Agent: Great! Let's get your details to sign you up 🚀")
        state["step"] = "collect_lead"

    return state


# Collects user details (name, email, platform)
# Only runs when user shows strong buying intent
# Finally triggers mock lead capture function
def lead_node(state):

    if state.get("step") == "collect_lead":

        if not state.get("name"):
            state["name"] = input("Name: ")

        if not state.get("email"):
            state["email"] = input("Email: ")

        if not state.get("platform"):
            state["platform"] = input("Platform: ")

        print("\nLead captured successfully:")
        print(f"Name: {state['name']}")
        print(f"Email: {state['email']}")
        print(f"Platform: {state['platform']}")

        state["step"] = "done"

    return state

# Builds the LangGraph workflow
# Defines how data flows between intent → RAG → response → lead capture
def build_graph():

    graph = StateGraph(dict)

    graph.add_node("intent", intent_node)
    graph.add_node("rag", rag_node)
    graph.add_node("response", response_node)
    graph.add_node("lead", lead_node)

    graph.set_entry_point("intent")

    graph.add_edge("intent", "rag")
    graph.add_edge("rag", "response")

    graph.add_conditional_edges(
        "response",
        lambda s: "lead" if s.get("step") == "collect_lead" else END
    )

    graph.add_edge("lead", END)

    return graph.compile()

# Entry function for the whole system
# Takes user state and runs full agent workflow
def run_agent(state):
    graph = build_graph()
    return graph.invoke(state)