"""Business LangGraph workflow."""

from __future__ import annotations

from langgraph.graph import (
    END,
    StateGraph,
)

from src.agents.registry import (
    AgentRegistry,
)
from src.graphs.nodes import (
    BusinessGraphNodes,
)
from src.graphs.state import (
    BusinessGraphState,
)
from src.modules.assistant.emitter import StreamEmitter


def create_business_graph(
    registry: AgentRegistry,
    emitter: StreamEmitter | None = None,
):


    nodes = BusinessGraphNodes(
        registry=registry,
        emitter=emitter,
    )


    graph = StateGraph(
        BusinessGraphState,
    )


    graph.add_node(
        "supervisor",
        nodes.supervisor,
    )


    graph.add_node(
        "agents",
        nodes.execute_agents,
    )


    graph.add_node(
        "response",
        nodes.respond,
    )


    graph.set_entry_point(
        "supervisor",
    )


    graph.add_conditional_edges(
        "supervisor",
        nodes.route,
        {
            "agents": "agents",
            "response": "response",
        },
    )


    graph.add_edge(
        "agents",
        "response",
    )


    graph.add_edge(
        "response",
        END,
    )


    return graph.compile()