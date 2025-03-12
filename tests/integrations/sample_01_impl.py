"""This file was generated using `langgraph-gen` version 0.0.3.

This file provides a placeholder implementation for the corresponding stub.

Replace the placeholder implementation with your own logic.
"""

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
        ("Node_1", Node_1),
        ("Node_2", Node_2),
        ("Node_3", Node_3),
        ("conditional_edge", conditional_edge),
    ],
)

compiled_agent = agent.compile()

print(compiled_agent.invoke({"foo": "bar"}))
