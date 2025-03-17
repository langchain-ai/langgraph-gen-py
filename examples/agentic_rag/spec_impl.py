"""This file was generated using `langgraph-gen` version 0.0.4.

This file provides a placeholder implementation for the corresponding stub.

Replace the placeholder implementation with your own logic.
"""

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
    ],
)

compiled_agent = agent.compile()

print(compiled_agent.invoke({"foo": "bar"}))
