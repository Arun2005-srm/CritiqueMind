# graph.py
from langgraph.graph import StateGraph, START, END
from state import AdvancedPipelineState
from nodes import writer_node, critic_node, synthesizer_node, route_governor

# Build and assemble the workflow blueprint
workflow = StateGraph(AdvancedPipelineState)

# Register specialized processing units
workflow.add_node("writer", writer_node)
workflow.add_node("critic", critic_node)
workflow.add_node("synthesizer", synthesizer_node)

# Map hard runtime wiring
workflow.add_edge(START, "writer")
workflow.add_edge("writer", "critic")

# Configure dynamic conditional routing mechanics out of the critic node
workflow.add_conditional_edges(
    "critic",
    route_governor,
    {
        "healthy_exit": END,
        "trigger_circuit_breaker": "synthesizer",
        "continue_iteration": "writer"
    }
)

workflow.add_edge("synthesizer", END)

# Compile into an executable application interface
app = workflow.compile()