from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class AgentState(TypedDict):
    messages: list
    next_agent: str
    final_output: str

# Define agent nodes
def code_agent(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}

def review_agent(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response], "final_output": response}

# Build the graph
graph = StateGraph(AgentState)
graph.add_node("code", code_agent)
graph.add_node("review", review_agent)
graph.add_node("human_approval", human_interrupt)

graph.set_entry_point("code")
graph.add_edge("code", "human_approval")

# Conditional: only proceed to review if approved
def approval_router(state: AgentState) -> Literal["review", "code"]:
    if state.get("approved"):
        return "review"
    return "code"

graph.add_conditional_edges("human_approval", approval_router)
graph.add_edge("review", END)

app = graph.compile()
result = app.invoke({"messages": ["Write a quicksort implementation"]})
