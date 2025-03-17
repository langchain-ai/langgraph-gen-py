"""This is an automatically generated file. Do not modify it.

This file was generated using `langgraph-gen` version 0.0.4.
To regenerate this file, run `langgraph-gen` with the source `yaml` file as an argument.

Usage:

1. Add the generated file to your project.
2. Create a new agent using the stub.

Below is a sample implementation of the generated stub:

```python
from typing_extensions import TypedDict

from spec import AgenticRag

class SomeState(TypedDict):
    # define your attributes here
    foo: str

# Define stand-alone functions
def agent(state: SomeState) -> dict:
    print("In node: agent")
    return {
        # Add your state update logic here
    }


def retrieve(state: SomeState) -> dict:
    print("In node: retrieve")
    return {
        # Add your state update logic here
    }


def rewrite(state: SomeState) -> dict:
    print("In node: rewrite")
    return {
        # Add your state update logic here
    }


def generate(state: SomeState) -> dict:
    print("In node: generate")
    return {
        # Add your state update logic here
    }


def is_relevant(state: SomeState) -> str:
    print("In condition: is_relevant")
    raise NotImplementedError("Implement me.")


agent = AgenticRag(
    state_schema=SomeState,
    impl=[
        ("agent", agent),
        ("retrieve", retrieve),
        ("rewrite", rewrite),
        ("generate", generate),
        ("is_relevant", is_relevant),
    ]
)

compiled_agent = agent.compile()

print(compiled_agent.invoke({"foo": "bar"}))
"""

from typing import Callable, Any, Optional, Type

from langgraph.constants import START, END  # noqa: F401
from langgraph.graph import StateGraph


def AgenticRag(
    *,
    state_schema: Optional[Type[Any]] = None,
    config_schema: Optional[Type[Any]] = None,
    input: Optional[Type[Any]] = None,
    output: Optional[Type[Any]] = None,
    impl: list[tuple[str, Callable]],
) -> StateGraph:
    """Create the state graph for AgenticRag."""
    # Declare the state graph
    builder = StateGraph(
        state_schema, config_schema=config_schema, input=input, output=output
    )

    nodes_by_name = {name: imp for name, imp in impl}

    all_names = set(nodes_by_name)

    expected_implementations = {
        "agent",
        "retrieve",
        "rewrite",
        "generate",
        "is_relevant",
    }

    missing_nodes = expected_implementations - all_names
    if missing_nodes:
        raise ValueError(f"Missing implementations for: {missing_nodes}")

    extra_nodes = all_names - expected_implementations

    if extra_nodes:
        raise ValueError(
            f"Extra implementations for: {extra_nodes}. Please regenerate the stub."
        )

    # Add nodes
    builder.add_node("agent", nodes_by_name["agent"])
    builder.add_node("retrieve", nodes_by_name["retrieve"])
    builder.add_node("rewrite", nodes_by_name["rewrite"])
    builder.add_node("generate", nodes_by_name["generate"])

    # Add edges
    builder.add_edge("agent", "retrieve")
    builder.add_conditional_edges(
        "retrieve",
        nodes_by_name["is_relevant"],
        [
            "rewrite",
            "generate",
        ],
    )
    builder.add_edge("rewrite", "agent")
    builder.add_edge("generate", END)
    builder.set_entry_point("agent")
    return builder
