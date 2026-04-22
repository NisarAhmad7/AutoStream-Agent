from agent import run_agent
from state import AgentState

print("Agent started...\n")

state: AgentState = {
    "user_input": "",
    "intent": "",
    "response": "",
    "step": "",
    "name": None,
    "email": None,
    "platform": None
}

while True:

    state["user_input"] = input("User: ")

    # manual lead collection
    if state.get("step") == "collecting" and not state.get("name"):
        state["name"] = input("Name: ")
        state["email"] = input("Email: ")
        state["platform"] = input("Platform: ")

    state = run_agent(state)

    print("Agent:", state["response"])