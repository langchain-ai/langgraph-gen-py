"""This file was generated using `langgraph-gen` version 0.0.4.

This file provides a placeholder implementation for the corresponding stub.

Replace the placeholder implementation with your own logic.
"""

from typing_extensions import TypedDict

from spec import RagWorkflow


class SomeState(TypedDict):
    # define your attributes here
    foo: str


# Define stand-alone functions
def retrieve(state: SomeState) -> dict:
    print("In node: retrieve")
    return {
        # Add your state update logic here
    }


def generate(state: SomeState) -> dict:
    print("In node: generate")
    return {
        # Add your state update logic here
    }


agent = RagWorkflow(
    state_schema=SomeState,
    impl=[
        ("retrieve", retrieve),
        ("generate", generate),
    ],
)

compiled_agent = agent.compile()

print(compiled_agent.invoke({"foo": "bar"}))
