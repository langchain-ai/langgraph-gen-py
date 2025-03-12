"""This is an automatically generated file. Do not modify it.

This file was generated using `langgraph-gen` version 0.0.3.
To regenerate this file, run `langgraph-gen` with the source `yaml` file as an argument.

Usage:

1. Add the generated file to your project.
2. Create a new agent using the stub.

Below is a sample implementation of the generated stub:

```python
from typing_extensions import TypedDict

from sample_01 import create_agent

class SomeState(TypedDict):
    # define your attributes here
    foo: str

# Define stand-alone functions
def Node_1(state: SomeState) -> dict:
    print("In node: Node 1")
    return {
        # Add your state update logic here
    }


def Node_2(state: SomeState) -> dict:
    print("In node: Node 2")
    return {
        # Add your state update logic here
    }


def Node_3(state: SomeState) -> dict:
    print("In node: Node 3")
    return {
        # Add your state update logic here
    }


def conditional_edge(state: SomeState) -> str:
    print("In condition: conditional_edge")
    raise NotImplementedError("Implement me.")


agent = create_agent(
    state_schema=SomeState,
    impl=[
        ("Node 1", Node_1),
        ("Node 2", Node_2),
        ("Node 3", Node_3),
        ("conditional_edge", conditional_edge),
    ]
)

compiled_agent = agent.compile()

print(compiled_agent.invoke({"foo": "bar"}))
"""

from typing import Callable, Any, Optional, Type

from langgraph.constants import START, END
from langgraph.graph import StateGraph


def create_agent(
    *,
    state_schema: Optional[Type[Any]] = None,
    config_schema: Optional[Type[Any]] = None,
    input: Optional[Type[Any]] = None,
    output: Optional[Type[Any]] = None,
    impl: list[tuple[str, Callable]],
) -> StateGraph:
    """Create the state graph for create_agent."""
    # Declare the state graph
    builder = StateGraph(
        state_schema, config_schema=config_schema, input=input, output=output
    )

    nodes_by_name = {name: imp for name, imp in impl}

    all_names = set(nodes_by_name)

    expected_implementations = {
        "Node_1",
        "Node_2",
        "Node_3",
        "conditional_edge",
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
    builder.add_node("Node 1", nodes_by_name["Node_1"])
    builder.add_node("Node 2", nodes_by_name["Node_2"])
    builder.add_node("Node 3", nodes_by_name["Node_3"])

    # Add edges
    builder.add_edge(START, "Node 1")
    builder.add_edge("Node 3", END)
    builder.add_edge("Node 2", END)
    builder.add_conditional_edges(
        "Node 1",
        nodes_by_name["conditional_edge"],
        [
            "Node 2",
            "Node 3",
        ],
    )
    return builder
